from devrim._internals import _log

def _load_file(filename):
    with open(filename) as file_data:
        import json
        json_data = json.load(file_data)
        return json_data

def load(filename = 'host.json', hostname = None, port = None, dispatcher = None, nodes = None):
    is_needed = hostname == None or port  == None or nodes == None or len(nodes) == 0
    if not is_needed:
        return
    
    json_data = _load_file(filename)
    
    server_data = json_data["server"]
    port_data = port if port != None else server_data["port"]
    try:
        discipline_data = server_data["discipline"]
    except KeyError:
        discipline_data = 0

    if not isinstance(port_data, int):
        raise TypeError('port should be an integer: {0}'.format(port_data))

    from devrim.models import Configuration
    from devrim.dispatchers import Discipline, RoundRobinDispatcher, WeightedRoundRobin, LeastConnection
    config = Configuration()
    
    config.hostname = hostname if hostname != None else server_data["hostname"]
    config.port = port_data
    config.discipline = Discipline(discipline_data)
    

    if dispatcher == None:
        if config.discipline != Discipline.NONE:
            if config.discipline == Discipline.ROUNDROBIN:
                config.dispatcher = RoundRobinDispatcher(json_data, nodes)
            elif config.discipline == Discipline.WEIGHTEDROUNDROBIN:
                config.dispatcher = WeightedRoundRobin(json_data, nodes)
            elif config.discipline == Discipline.LEASTCONNECTION:
                config.discipline = LeastConnection(json_data, nodes)
        else: 
            config.dispatcher = RoundRobinDispatcher(json_data, nodes)
    
    config.nodes = config.dispatcher.nodes
    
    _log("info", "Configuration loaded")
    return config