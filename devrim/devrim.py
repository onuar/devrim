import http.client
from werkzeug.wrappers import Response, Request

from devrim._internals import _log, execstat
from devrim.dispatchers import Discipline,RoundRobinDispatcher

class Devrim:
    def __init__(self, dispatcher = None, hostname = None, port = 4242, nodes = None):
        self.hostname = hostname
        self.port = port
        self.nodes = nodes
        self.dispatcher = dispatcher

    def _load_configs(self):
        # load configs if needed
        from devrim.configurators import load as config_loader
        config = config_loader(hostname=self.hostname,port=self.port,dispatcher=self.dispatcher,nodes=self.nodes)
        self.hostname = config.hostname
        self.port = config.port
        self.nodes = config.nodes
        self.dispatcher = config.dispatcher

    def _iterform(self, multidict):
        for key in multidict.keys():
            for value in multidict.getlist(key):
                yield (key.encode("utf8"), value.encode("utf8"))

    def _convert_to_external_response(self, internal_response):
        content = internal_response.read()
        status = internal_response.status
        content_type = internal_response.getheader('content-type')

        response = Response(content, status=status, content_type=content_type)    
        response.headers.clear()

        for key, value in internal_response.getheaders():
            response.headers[key] = value

        return response

    @execstat
    def _internal_request(self, connection):
        internal_response = connection.getresponse()
        return internal_response

    @Request.application
    def _handler(self, request):
        node = self.dispatcher.get_next_one()
        # _log('dev', node)
        req_headers = dict(request.headers)
    
        if request.method == "POST" or request.method == "PUT":
            form_data = list(self._iterform(request.form))
            # form_data = urllib.parse.urlencode(form_data)
            req_headers["Content-Length"] = len(form_data)
        else:
            form_data = None

        connection = http.client.HTTPConnection(node)
        connection.request(request.method, request.full_path, body = form_data, headers = req_headers)
        internal_response = self._internal_request(connection)
        response = self._convert_to_external_response(internal_response)
        # response = Response(str(self.nodes) + " >>>"+ node, status=200, content_type="text/html") # test line
        return response

    def run(self):
        self._load_configs()
        from werkzeug.serving import run_simple
        _log("info", "{0}:{1} => {2}".format(self.hostname, self.port, str(self.nodes)))
        run_simple(self.hostname, self.port, self._handler)

    def stop(self):
        # if it's possible, stop werkzeug service
        pass