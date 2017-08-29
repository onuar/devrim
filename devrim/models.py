class Configuration:
    def __init__(self, hostname = None, port = None, dispatcher = None, nodes = None, discipline = None):
        self.hostname = hostname
        self.port = port
        self.nodes = nodes
        self.discipline = discipline
        self.dispatcher = dispatcher