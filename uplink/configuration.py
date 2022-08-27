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

from logging import getLogger

logger = getLogger(__name__)


class Configuration:

    def __init__(self, configuration):

        self.__configuration = configuration
        self.__database_host = None
        self.__database_name = None
        self.__database_password = None
        self.__database_user = None
        self.__httpserver_framework = None
        self.__httpserver_host = '0.0.0.0'
        self.__httpserver_port = 8080
        self.__interval = '60'
        self.__log_count = 5
        self.__log_file = None
        self.__log_level = 'info'
        self.__log_size = 10485760,
        self.__pid_file = '/tmp/uplink.pid'
        self.__run_mode = None
        self.__uplinks = None

        self.__env = {}

        if'database_host' in self.__configuration:
            self.__database_host = self.__configuration['database_host']
        else:
            raise Exception('database_host required!')

        if 'database_name' in self.__configuration:
            self.__database_name = self.__configuration['database_name']
        else:
            raise Exception('database_name required!')

        if 'database_password' in self.__configuration:
            self.__database_password = self.__configuration['database_password']
        else:
            raise Exception('database_password required!')

        if 'database_user' in self.__configuration:
            self.__database_user = self.__configuration['database_user']
        else:
            raise Exception('database_user required!')

        if 'httpserver_framework' in self.__configuration:
            self.__httpserver_framework = self.__configuration['httpserver_framework']

        if 'httpserver_host' in self.__configuration:
            self.__httpserver_host = self.__configuration['httpserver_host']

        if 'httpserver_port' in self.__configuration:
            self.__httpserver_port = self.__configuration['httpserver_port']

        if 'interval' in self.__configuration:
            self.__interval = self.__configuration['interval']

        if 'log_level' in self.__configuration:
            self.__log_level = self.__configuration['log_level']

        if 'run_mode' in self.__configuration:
            self.__run_mode = self.__configuration['run_mode']

        if 'uplinks' in self.__configuration:
            self.__uplinks = self.__configuration['uplinks']
        else:
            raise Exception('uplinks required!')

    def get_database_host(self):
        return self.__database_host

    def get_database_name(self):
        return self.__database_name

    def get_database_password(self):
        return self.__database_password

    def get_database_user(self):
        return self.__database_user

    def get_env(self):
        return self.__env

    def get_env_var(self, name):
        return self.__env[name]

    def set_env_var(self, name, value):
        self.__env[name] = value

    def get_httpserver_framework(self):
        return self.__httpserver_framework

    def get_httpserver_host(self):
        return self.__httpserver_host

    def get_httpserver_port(self):
        return self.__httpserver_port

    def get_interval(self):
        return self.__interval

    def set_interval(self, interval):
        self.__interval = interval

    def get_log_level(self):
        return self.__log_level

    def get_pid_file(self):
        return self.__pid_file

    def get_mode(self):
        return self.__run_mode

    def get_uplink(self, uplink):
        return self.__uplinks[uplink]

    def get_uplinks(self):
        return self.__uplinks
