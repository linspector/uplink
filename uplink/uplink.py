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

            logger.info(str(uplink['provider'] + ' ' + self.status + ' (ip: ' +
                            fc.external_ip + ')'))

            model = Model(self.configuration)

            database = Database(self.configuration)
            database.write_to_db(fc, uplink['ip'], uplink['provider'], self.status)

        except Exception as err:
            message = str('error when getting data from ' + uplink['ip'] + ': {0}')
            logger.error(str(message.format(err)))

    def run(self):
        if self.configuration.get_env_var('_server'):
            if self.configuration.get_httpserver_framework() == 'bottle':
                from uplink.server_bottle import Server
                s = Server(self.configuration)
                st = Thread(target=s.run, daemon=True)
                st.start()
            elif self.configuration.get_httpserver_framework() == 'cherrypy':
                from uplink.server_cherrypy import Server
                s = Server(self.configuration)
                st = Thread(target=s.run, daemon=True)
                st.start()
            elif self.configuration.get_httpserver_framework() == 'pyramid':
                from uplink.server_pyramid import Server
                s = Server(self.configuration)
                st = Thread(target=s.run, daemon=True)
                st.start()
        while True:
            for i in range(len(self.configuration.get_uplinks())):
                ut = Thread(target=self.fetch_data, daemon=True, args=(i,))
                ut.start()
            time.sleep(self.configuration.get_interval())
