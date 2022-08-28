# Copyright (c) 2021 Johannes Findeisen <you@hanez.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice (including the next
# paragraph) shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
# OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# TODO: Switch all SQL stuff to SQLAlchemy using the uplink.database Database class
# TODO: Make the use of a database optional and only output to stdout and/or in a logfile (use rich
#  for colorizing the std output (https://github.com/Textualize/rich)); Output to a CSV file should
#  be optional too.

import calendar
import socket
import time

from fritzconnection.lib.fritzstatus import FritzStatus
from logging import getLogger
from threading import Thread
from uplink.daemon import Daemon
from uplink.database import Database
from uplink.model import Model

logger = getLogger(__name__)


class Uplink(Daemon):

    def __init__(self, pid_file, configuration):
        super().__init__(pid_file)
        self.configuration = configuration
        self.date = None
        self.time = None
        self.status = None

    def fetch_data(self, i):
        timestamp = calendar.timegm(time.gmtime())
        local_time = time.localtime(timestamp)
        self.date = time.strftime('%Y-%m-%d', local_time)
        self.time = time.strftime('%H:%M:%S', local_time)

        uplink = self.configuration.get_uplink(i)
        try:
            fc = FritzStatus(address=uplink['ip'],
                             password=uplink['password'])
            if fc.is_connected:
                self.status = 'UP'
            else:
                self.status = 'DOWN'

            logger.info(str(uplink['provider'] + ' (uplink IP: ' + fc.external_ip + ') ' +
                            self.status))

            model = Model(self.configuration)
            model.set_date(self.date)
            model.set_external_ip(fc.external_ip)
            model.set_external_ipv6(fc.external_ipv6)
            model.set_internal_ip(uplink['ip'])
            model.set_is_connected(fc.is_connected)
            model.set_is_linked(fc.is_linked)
            model.set_message(self.status)
            model.set_model_name(fc.modelname)
            model.set_provider(uplink['provider'])
            model.set_source_host(socket.gethostname())
            model.set_str_max_bit_rate_down(fc.str_max_bit_rate[1])
            model.set_str_max_bit_rate_up(fc.str_max_bit_rate[0])
            model.set_str_max_linked_bit_rate_down(fc.str_max_linked_bit_rate[1])
            model.set_str_max_linked_bit_rate_up(fc.str_max_linked_bit_rate[0])
            model.set_str_transmission_rate_down(fc.str_transmission_rate[1])
            model.set_str_transmission_rate_up (fc.str_transmission_rate[0])
            model.set_system_version(fc.fc.system_version)
            model.set_time(self.time)
            model.set_timestamp(timestamp)
            model.set_uptime(fc.connection_uptime)

            database = Database(self.configuration)
            database.write_model_to_db(model)

        except Exception as err:
            message = str('error when getting data from ' + uplink['ip'] + ': {0}')
            logger.error(str(message.format(err)))

    def run(self):
        if self.configuration.get_env_var('_server'):
            if self.configuration.get_httpserver_framework() == 'bottle':
                from uplink.server_bottle import Server
                s = Server(self.configuration)
                st = Thread(target=s.run_server, daemon=True)
                st.start()
            elif self.configuration.get_httpserver_framework() == 'cherrypy':
                from uplink.server_cherrypy import Server
                s = Server(self.configuration)
                st = Thread(target=s.run_server, daemon=True)
                st.start()
            elif self.configuration.get_httpserver_framework() == 'pyramid':
                from uplink.server_pyramid import Server
                s = Server(self.configuration)
                st = Thread(target=s.run_server, daemon=True)
                st.start()
        while True:
            for i in range(len(self.configuration.get_uplinks())):
                ut = Thread(target=self.fetch_data, daemon=True, args=(i,))
                ut.start()
            time.sleep(self.configuration.get_interval())