# Copyright (c) 2022 Johannes Findeisen <you@hanez.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice (including the next
# paragraph) shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
# OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json

from logging import getLogger
from pyramid.config import Configurator
from pyramid.response import Response
from wsgiref.simple_server import make_server

logger = getLogger(__name__)


class Server:

    def __init__(self, configuration):
        self.__configuration = configuration

    def config(self, request):
        return Response(config=json.dumps(vars(self.__configuration), sort_keys=True, indent=4))

    def run_server(self):
        with Configurator() as config:
            config.add_route('config', '/')
            config.add_view(self.config, route_name='config')
            app = config.make_wsgi_app()
        server = make_server(self.__configuration.get_httpserver_host(),
                             self.__configuration.get_httpserver_port(), app)
        server.serve_forever()
