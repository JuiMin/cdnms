import json
import logging

from models import Room, Card, Codenames, Team

CDNMS_MODELS = (Room, Card, Codenames, Team)


class CDNMSEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CDNMS_MODELS):
            logging.info(type(obj))
            logging.info(dir(obj))
            o = dict()
            for k in obj.__slots__:
                try:
                    o[k] = self.default(obj.__getattribute__(k))
                except:
                    o[k] = "ERROR"
            return o
        elif isinstance(obj, list):
            return [self.default(a) for a in obj]
        elif isinstance(obj, dict):
            return {k: self.default(v) for k, v in obj.items()}
        elif isinstance(obj, (str, int)):
            return obj
        else:
            return str(obj)
