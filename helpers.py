import json
import logging
from typing import List

logger = logging.getLogger()
class ServerAPI(object):
    host = ''
    def __init__(self, host):
        self.host = host
        assert host is not None, "Define a base URL for the Gitlab Server"
        if not self.host.endswith('/'):
            self.host += '/'
def get_list(response, Model):
    """
    Pseudo-code à la DRF serializers
    :param response: une réponse de simple-rest-client
    :param Model: une classe avec les attributs qui seront remplis
    :return: une liste d'instances de Model
    """
    list = []
    for obj in response.body:
        list.append(Model(**obj))
    return list

class DataModel(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs) #pythonista qui utilise les arguments du constructeur pour remplir les attributs de l'objet

def load_config(args):
    try:
        with open(args.config_file, 'r') as json_config:
            try:
                data = json.load(json_config)
                args.__dict__.update(data)
            except (json.JSONDecodeError):
                logger.exception("Error readind file {}".format(args.config_file))
    except FileNotFoundError:
        pass