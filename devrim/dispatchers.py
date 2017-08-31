from enum import Enum, unique
from operator import itemgetter

from devrim.exceptions import NodesNotFoundException
from devrim._internals import _log

class BaseDispatcher:
    pass

class RoundRobinDispatcher(BaseDispatcher):
    def __init__(self, json_data, nodes = None):
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
    def __init__(self, json_data, nodes = None):
        self.nodes = nodes
        self.json_data = json_data
        self._internal_nodes = []
        self.reset_count = 0
        self.req_counter = 0
        self._load_configs()
    
    def _load_configs(self):
        self.nodes = self.nodes if self.nodes != None else list(self.json_data["nodes"])
        self._internal_nodes = sorted([{'id':_, 'node':self.nodes[_]['node'], 'used':0, 'max':self.nodes[_]['weight']} for _ in range(len(self.nodes))], key=itemgetter('id'))
        self.reset_count = sum(row['max'] for row in self._internal_nodes)

    def reset_used_stat(self):
        for row in self._internal_nodes:
            row['used'] = 0

    def get_next_one(self):
        self.req_counter += 1
        availables = sorted(filter(lambda row: row['used'] < row['max'], self._internal_nodes), key=itemgetter('id'))
        availables[0]['used'] += 1
        node = availables[0]

        if self.req_counter == self.reset_count:
            self.reset_used_stat()

        # _log('dev', list(availables))
        return node['node']


class StickyClient(BaseDispatcher):
    def __init__(self, nodes):
        self.nodes = nodes

@unique
class Discipline(Enum):
    NONE = 0
    ROUNDROBIN = 1
    WEIGHTEDROUNDROBIN = 2
    STICKYCLIENT = 3

