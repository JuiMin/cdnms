from enum import Enum
import json
import logging

from datastore import StorageResponse
from models import Room, Card, Codenames
from handler_util import CDNMSCommand, CDNMSCommandResult, CDNMSResponse

datastore_objs = (StorageResponse,)
cdnms_model_objs = (Room, Card, Codenames)
handler_objs = (CDNMSResponse, CDNMSCommand, CDNMSCommandResult)
builtin_objs = datastore_objs + cdnms_model_objs + handler_objs


class CDNMSEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, builtin_objs):
            o = dict()
            for k in obj.__slots__:
                try:
                    o[k] = self.default(obj.__getattribute__(k))
                except Exception as e:
                    logging.info(str(e))
                    o[k] = str(e)
            return o
        elif isinstance(obj, (set, list)):
            return [self.default(a) for a in obj]
        elif isinstance(obj, dict):
            return {k: self.default(v) for k, v in obj.items()}
        elif isinstance(obj, (str, int)):
            return obj
        elif isinstance(obj, Enum):
            return obj.name
        elif obj == None:
            return None
        else:
            return str(obj)
