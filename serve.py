import os
import cgi
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from routes import RoutePlan
from simple_traffic_learning import QAgent

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HEADER_MAP = {
    'png': 'image/png',
    'jpg': 'image/jpg',
    'js': 'text/javascript',
    'css': 'text/css',
    '': 'text/html'
}


class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handles the GET requests."""
        content, content_type = handle_request(self.path)

        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])

        # convert pdict[boundary] to bytes
        pdict['boundary'] = pdict['boundary'].encode("utf-8")
        pdict['CONTENT-LENGTH'] = 10000

        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
        else:
            # only form-data is accepted
            fields = {}

        shape, connections = parse_form_data(fields)
        response_code = 200

        rp = RoutePlan((shape, shape), connections, shape * 2)
        rp.form_rewards()

        qagent = QAgent(0.75, 0.9, rp)
        loc_route, state_route = qagent.training((0, 0), (shape - 1, shape - 1),
                                                 1000)

        response_data = json.dumps({"route": state_route})

        # Send the "message" field back as the response.
        self.send_response(response_code, response_data)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'')


def handle_request(path):
    """Returns the content type and the content according to the given path."""
    # extention is blank if no resource is requested
    extention = path.split('/')[-1].split('.')[-1]

    if extention in ["jpg", "png"]:
        # read images as binary files
        with open(BASE_DIR + path, 'rb') as f:
            content = f.read()
    elif extention in ['css', 'js']:
        # encode strings
        with open(BASE_DIR + path, 'r') as f:
            content = f.read().encode('utf-8')
    else:
        with open(BASE_DIR + '/templates/paths.html') as f:
            content = f.read().encode('utf-8')

    try:
        # content type according to the extention
        content_type = HEADER_MAP[extention]
    except KeyError:
        content_type = 'text/plain'

    return content, content_type


def parse_form_data(data):
    """Decomposes the given form-data and returns a steps list."""
    # data = {'steps': ['right,left']}
    connection_param = json.loads(data['connections'][0])
    shape = json.loads(data['shape'][0])
    return shape, connection_param


def run():
    try:
        # Create a web server and define the handler to manage the
        # incoming request
        server = HTTPServer(('', 8000), myHandler)

        # Wait forever for incoming http requests
        server.serve_forever()

    except KeyboardInterrupt:
        server.socket.close()


if __name__ == '__main__':
    run()
