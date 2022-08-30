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

        self.__base_configuration = None
        self.__database_host = None
        self.__database_name = None
        self.__database_password = None
        self.__database_user = None
        # environment vars which can be set dynamically at runtime. these vars are shared across all
        # objects and readable and writable by all of them.
        self.__env = {}
        self.__httpserver = False
        self.__httpserver_host = '0.0.0.0'
        self.__httpserver_port = 1042
        self.__interval = 60
        self.__log_count = 1
        self.__log_file = None
        self.__log_level = None
        self.__log_size = 0
        self.__pid_file = '/tmp/uplink.pid'
        self.__run_mode = 'cron'
        self.__speedtest = False
        self.__speedtest_interval = 3600
        self.__speedtest_url = "https://unixpeople.org/uplink.test"
        self.__uplinks = None

        if 'database_host' in self.__configuration:
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

        if 'httpserver' in self.__configuration:
            self.__httpserver = self.__configuration['httpserver']

        if 'httpserver_host' in self.__configuration:
            self.__httpserver_host = self.__configuration['httpserver_host']

        if 'httpserver_port' in self.__configuration:
            self.__httpserver_port = self.__configuration['httpserver_port']

        if 'interval' in self.__configuration:
            self.__interval = self.__configuration['interval']

        if 'log_count' in self.__configuration:
            self.__log_count = self.__configuration['log_count']

        if 'log_file' in self.__configuration:
            self.__log_file = self.__configuration['log_file']

        if 'log_level' in self.__configuration:
            self.__log_level = self.__configuration['log_level']

        if 'log_size' in self.__configuration:
            self.__log_size = self.__configuration['log_size']

        if 'pid_file' in self.__configuration:
            self.__pid_file = self.__configuration['pid_file']

        if 'run_mode' in self.__configuration:
            self.__run_mode = self.__configuration['run_mode']

        if 'speedtest' in self.__configuration:
            self.__speedtest = self.__configuration['speedtest']

        if 'speedtest_interval' in self.__configuration:
            self.__speedtest_interval = self.__configuration['speedtest_interval']

        if 'speedtest_url' in self.__configuration:
            self.__speedtest_url = self.__configuration['speedtest_url']

        if 'uplinks' in self.__configuration:
            self.__uplinks = self.__configuration['uplinks']
        else:
            raise Exception('uplinks required!')

    # get methods
    def get_base_configuration(self):
        return self

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

    def get_env_var(self, key):
        if key in self.__env:
            return self.__env[key]

    def get_httpserver(self):
        return self.__httpserver

    def get_httpserver_host(self):
        return self.__httpserver_host

    def get_httpserver_port(self):
        return self.__httpserver_port

    def get_interval(self):
        return self.__interval

    def get_log_file(self):
        return self.__log_file

    def get_log_count(self):
        return self.__log_count

    def get_log_level(self):
        return self.__log_level

    def get_log_size(self):
        return self.__log_size

    def get_pid_file(self):
        return self.__pid_file

    def get_mode(self):
        return self.__run_mode

    def get_speedtest(self):
        return self.__speedtest

    def get_speedtest_interval(self):
        return self.__speedtest_interval

    def get_speedtest_url(self):
        return self.__speedtest_url

    def get_uplink(self, uplink):
        return self.__uplinks[uplink]

    def get_uplinks(self):
        return self.__uplinks

    # set methods
    def set_env_var(self, key, value):
        self.__env[key] = value

    def set_httpserver(self, value):
        self.__httpserver = value

    def set_interval(self, interval):
        self.__interval = interval

    def set_log_file(self, log_file):
        self.__log_file = log_file
