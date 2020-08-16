"""
handlers.py defines handler wrapping implementations to ease endpoint devs.
"""
from http import HTTPStatus
from inspect import signature
import json
import logging
from typing import Any, Callable, Dict, Optional

import tornado.web
import tornado.websocket

from debug_endpoints import DEBUG_ENDPOINT_MAPPING
from endpoints import ENDPOINT_MAPPING
from handler_util import CDNMSCommand, CDNMSCommandResult, CDNMSResponse
from serializer import CDNMSEncoder


# Dyanmic Handlers
class CDNMSRequestHandler(tornado.web.RequestHandler):
    def initialize(self, endpoints: Dict):
        self.get_method = endpoints.get("GET", None)
        self.post_method = endpoints.get("POST", None)
        get_query_params = []
        if self.get_method:
            get_query_params = signature(self.get_method).parameters
        self.get_allowed_qargs = get_query_params

    def get(self, *args, **kwargs):
        if not self.get_method:
            return super().get()
        self.set_header("Content-Type", "application/json")
        if self.request.query_arguments:
            for query_arg in self.get_allowed_qargs:
                value = self.get_query_argument(query_arg, None)
                if value:
                    kwargs[query_arg] = str(value)
        try:
            logging.info(kwargs)
            resp: CDNMSResponse = self.get_method(*args, **kwargs)
            self.set_status(resp.status)
            self.write(json.dumps(resp.body, cls=CDNMSEncoder))
        except TypeError as e:
            self.write_error(
                HTTPStatus.BAD_REQUEST.value, exc_info=str(e),
            )
        except Exception as e:
            self.write_error(
                HTTPStatus.INTERNAL_SERVER_ERROR.value, exc_info=str(e),
            )

    def post(self, *args, **kwargs):
        if not self.post_method:
            return super().post()
        if self.request.body:
            try:
                body = json.loads(self.request.body)
                kwargs.update({k: str(v) for k, v in body.items()})
            except Exception as e:
                self.write_error(
                    HTTPStatus.BAD_REQUEST.value, exc_info=str(e),
                )
                return
        try:
            resp: CDNMSResponse = self.post_method(*args, kwargs)
            self.set_status(resp.status)
            self.write(json.dumps(resp.body, cls=CDNMSEncoder))
        except TypeError as e:
            self.write_error(
                HTTPStatus.BAD_REQUEST.value, exc_info=str(e),
            )
        except Exception as e:
            self.write_error(
                HTTPStatus.INTERNAL_SERVER_ERROR.value, exc_info=str(e),
            )


class CDNMSWebsocketHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, endpoints: Dict):
        self.default_method = endpoints.get("DEFAULT", None)

    def open(self):
        logging.info("Opening Socket Connection.")

    def close(self, room_id):
        logging.info("Closing socket Connection.")

    def on_message(self, message):
        if not message:
            self.write_error(HTTPStatus.BAD_REQUEST.value)
        command = None
        try:
            command = CDNMSCommand(json.loads(message))
        except Exception as e:
            logging.error(str(e), exc_info=True)
            self.write_message(str(e))
        if command:
            res: CDNMSCommandResult = self.default_method(command, self)
        else:
            res = CDNMSCommandResult(False, {})
        if not res.success:
            self.write_message(json.dumps(res, cls=CDNMSEncoder))


# Manual Route Handlers
class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(HTTPStatus.OK)
        self.render(
            "index.html",
            static_url=self.static_url,
            full_url=self.request.full_url(),
        )


# Default with the builtin handlers
cdnms_routes = [(r"/", RootHandler)]

# Possible handlers
HANDLER_MAPPING = {
    "response": CDNMSRequestHandler,
    "websocket": CDNMSWebsocketHandler,
}

# Construct route mapping to be expanded in tornado
used_mappings = (ENDPOINT_MAPPING, DEBUG_ENDPOINT_MAPPING)
for mapping in used_mappings:
    for handler_type in mapping:
        try:
            handler_class = HANDLER_MAPPING[handler_type]
            for target, endpoints in mapping[handler_type].items():
                cdnms_routes.append(
                    (target, handler_class, dict(endpoints=endpoints))
                )
        except Exception as e:
            logging.error(str(e), exc_info=True)
