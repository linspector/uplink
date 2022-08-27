# Copyright (c) 2021 Johannes Findeisen <you@hanez.org>
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

# TODO: Switch all SQL stuff to SQLAlchemy using the uplink.database Database class
# TODO: Make the use of a database optional and only output to stdout and/or in a logfile (use rich
#  for colorizing the std output (https://github.com/Textualize/rich))

import calendar
import pymysql
import socket
import sys
import time

from uplink.configuration import Configuration
from uplink.daemon import Daemon
from uplink.database import Database
from fritzconnection.lib.fritzstatus import FritzStatus
from logging import getLogger
from threading import Thread

logger = getLogger(__name__)


class Uplink(Daemon):

    def __init__(self, pid_file, config, configuration):
        super().__init__(pid_file)
        #self.config = config
        self.configuration = configuration
        self.date = None
        self.time = None
        self.status = None

    def get_time(self):
        return self.time

    def get_status(self):
        return self.status

    def fetch_data(self, config, uplink):
        try:
            con = pymysql.connect(host=self.configuration.get_database_host(),
                                  user=self.configuration.get_database_user(),
                                  password=self.configuration.get_database_password(),
                                  database=self.configuration.get_database_name())
        except Exception as err:
            logger.error(str("database connection failed: {0}".format(err)))

        timestamp = calendar.timegm(time.gmtime())
        local_time = time.localtime(timestamp)
        self.date = time.strftime("%Y-%m-%d", local_time)
        self.time = time.strftime("%H:%M:%S", local_time)

        try:
            fc = FritzStatus(address=config["uplinks"][uplink]["ip"],
                             password=config["uplinks"][uplink]["password"])
        except Exception as err:
            logger.error(str(str(err) + " on device with ip: " + config["uplinks"][uplink]["ip"]))
            # TODO: Fix to long lines and make the SQL statement more readable
            sql = 'INSERT INTO log (timestamp, date, time, internal_ip, is_linked, is_connected, provider, message, ' \
                  'source_host)  VALUES (\"' + str(timestamp) + '\",\"' + str(self.date) + '\",\"' + str(self.time) + '\",\"' + \
                  str(config["uplinks"][uplink]["ip"]) + '\",\"' + "0" + '\",\"' + "0" + '\",\"' + \
                  str(config["uplinks"][uplink]["provider"]) + '\",\"ERROR: ' + str(err) + '\",\"' + socket.gethostname() + \
                  '\")'

            logger.debug(str(sql))
            with con.cursor() as cur:
                cur.execute(sql)
            con.commit()
            sys.exit(1)

        if fc.is_connected:
            self.status = "UP"
        else:
            self.status = "DOWN"

        logger.info(str(config["uplinks"][uplink]["provider"] + " " + self.status))
        # TODO: Fix to long lines and make the SQL statement more readable
        sql = 'INSERT INTO log (timestamp, date, time, uptime, internal_ip, external_ip, external_ipv6, is_linked, ' \
              'is_connected, str_transmission_rate_up, str_transmission_rate_down, str_max_bit_rate_up, ' \
              'str_max_bit_rate_down, str_max_linked_bit_rate_up, str_max_linked_bit_rate_down, modelname, ' \
              'system_version, provider, message, source_host) VALUES (\"' + str(timestamp) + '\",\"' + str(self.date) + '\",\"' + \
              str(self.time) + '\",\"' + str(fc.connection_uptime) + '\",\"' + str(config["uplinks"][uplink]["ip"]) + '\",\"' + \
              str(fc.external_ip) + '\",\"' + str(fc.external_ipv6) + '\",\"' + str(int(fc.is_linked)) + '\",\"' + \
              str(int(fc.is_connected)) + '\",\"' + str(fc.str_transmission_rate[0]) + '\",\"' + \
              str(fc.str_transmission_rate[1]) + '\",\"' + str(fc.str_max_bit_rate[0]) + '\",\"' + \
              str(fc.str_max_bit_rate[1]) + '\",\"' + str(fc.str_max_linked_bit_rate[0]) + '\",\"' + \
              str(fc.str_max_linked_bit_rate[1]) + '\",\"' + str(fc.modelname) + '\",\"' + \
              str(fc.fc.system_version) + '\",\"' + str(config["uplinks"][uplink]["provider"]) + '\",\"' + self.status + '\",\"' + \
              socket.gethostname() + '\")'

        logger.debug(str(sql))
        with con.cursor() as cur:
            cur.execute(sql)
        con.commit()
        con.close()

    def run(self):
        if self.configuration.get_env_var("_server"):
            if self.config["httpserver_framework"] == "bottle":
                from uplink.server_bottle import Server
            else:
                from uplink.server_cherrypy import Server
            s = Server(self.config)
            st = Thread(target=s.run, daemon=True)
            st.start()

        while True:
            for i in range(len(self.config["uplinks"])):
                ut = Thread(target=self.fetch_data, daemon=True, args=(self.config, i))
                ut.start()
            time.sleep(self.configuration.get_interval())
