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

# TODO: Select a template engine for easy output creation. Mako preferred but need to
#  take a look at Jinja.

import cherrypy
import json

from logging import getLogger

logger = getLogger('uplink')


class HTTPServer:

    def __init__(self, configuration):
        self.__configuration = configuration

    @cherrypy.expose
    def index(self):
        return 'Hello world!'

    @cherrypy.expose
    def config(self):
        return '<!DOCTYPE html><html><head><title>[uplink] configuration</title><meta ' + \
               'http-equiv="refresh" content="60"></head><body><pre ' + \
               'style="border:2px solid black;background:#1d2021;color:#f0751a;">' + \
               json.dumps(vars(self.__configuration), sort_keys=True, indent=4) + \
               '</pre></body></html>'

    @cherrypy.expose
    def playground(self):
        return 'My Playground!'

    def run_server(self):
        conf = {
            '/': {
                #    'tools.sessions.on': True,
                #    'tools.staticdir.root': os.path.abspath(os.getcwd())
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            },
            '/config': {
                #    'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/html')],
            },
            '/playground': {
                #    'tools.staticdir.on': True,
                #    'tools.staticdir.dir': './public'
            }
        }
        #cherrypy.config.update({
        #    'global': {
        #        'engine.autoreload.on': False
        #    }
        #})
        cherrypy.config.update({
            'global': {
                'server.socket_host': self.__configuration.get_httpserver_host(),
                'server.socket_port': self.__configuration.get_httpserver_port(),
                'environment': 'production'
            }
        })
        cherrypy.tree.mount(root=None, config=conf)
        cherrypy.quickstart(self, '/', conf)
        #cherrypy.server.bus.exit(self)
