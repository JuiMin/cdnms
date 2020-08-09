from enum import Enum
import json
import logging

from models import Room, Card, Codenames

CDNMS_MODELS = (Room, Card, Codenames)


class CDNMSEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CDNMS_MODELS):
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
        else:
            return str(obj)
