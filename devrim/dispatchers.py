from enum import Enum, unique

from devrim.exceptions import NodesNotFoundException
from devrim._internals import _log

class BaseDispatcher:
    pass

class RoundRobinDispatcher(BaseDispatcher):
    def __init__(self, json_data, nodes):
        self.nodes = nodes
        self.json_data = json_data
        self._route_index = 0
        self._load_configs()
    
    def _load_configs(self):
        self.nodes = self.nodes if self.nodes != None else list(self.json_data["nodes"])

    def get_next_one(self):
        if len(self.nodes) == 0:
            raise NodesNotFoundException()
        
        _log("info", "Route index: {0}".format(self._route_index))
        next_route = self.nodes[self._route_index]
        self._route_index += 1 
        if self._route_index == len(self.nodes):
            self._route_index = 0
        return next_route

class WeightedRoundRobin(BaseDispatcher):
    def __init__(self, nodes, json_data):
        self.nodes = nodes
        self.json_data = json_data

class StickyClient(BaseDispatcher):
    def __init__(self, nodes):
        self.nodes = nodes

@unique
class Discipline(Enum):
    NONE = 0
    ROUNDROBIN = 1
    WEIGHTEDROUNDROBIN = 2
    STICKYCLIENT = 3

