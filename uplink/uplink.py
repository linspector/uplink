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


from logging import getLogger
import socket
import sys
import time
import calendar

try:
    from fritzconnection.fritzconnection.lib.fritzstatus import FritzStatus
except ImportError:
    from fritzconnection.lib.fritzstatus import FritzStatus

from threading import Thread
import pymysql
from uplink.daemon import Daemon

logger = getLogger(__name__)


class Uplink(Daemon):

    def __init__(self, pid_file, config):
        super().__init__(pid_file)
        self.pid_file = pid_file
        self.config = config
        self.date = None
        self.time = None
        self.status = None

    def fetch_data(self, config, inc):
        try:
            # TODO: Think about using a DB ORM (SQLAlchemy?) to make this program supporting different databases like
            #  sqlite and Postgres
            con = pymysql.connect(host=config["database_host"],
                                  user=config["database_user"],
                                  password=config["database_password"],
                                  database=config["database"])
        except Exception as err:
            logger.error(str("uplink: Database connection failed: " + str(err)))
            sys.exit(1)

        timestamp = calendar.timegm(time.gmtime())
        local_time = time.localtime(timestamp)
        self.date = time.strftime("%Y-%m-%d", local_time)
        self.time = time.strftime("%H:%M:%S", local_time)

        try:
            fc = FritzStatus(address=config["uplinks"][inc]["ip"], password=config["uplinks"][inc]["password"])
        except Exception as err:
            logger.error(str(str(err) + " on device with ip: " + config["uplinks"][inc]["ip"]))
            # TODO: Fix to long lines and make the SQL statement more readable
            sql = 'INSERT INTO log (timestamp, date, time, internal_ip, is_linked, is_connected, provider, message, ' \
                  'source_host)  VALUES (\"' + str(timestamp) + '\",\"' + str(self.date) + '\",\"' + str(self.time) + '\",\"' + \
                  str(config["uplinks"][inc]["ip"]) + '\",\"' + "0" + '\",\"' + "0" + '\",\"' + \
                  str(config["uplinks"][inc]["provider"]) + '\",\"ERROR: ' + str(err) + '\",\"' + socket.gethostname() + \
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

        logger.info(str(config["uplinks"][inc]["provider"] + " " + self.status))
        # TODO: Fix to long lines and make the SQL statement more readable
        sql = 'INSERT INTO log (timestamp, date, time, uptime, internal_ip, external_ip, external_ipv6, is_linked, ' \
              'is_connected, str_transmission_rate_up, str_transmission_rate_down, str_max_bit_rate_up, ' \
              'str_max_bit_rate_down, str_max_linked_bit_rate_up, str_max_linked_bit_rate_down, modelname, ' \
              'system_version, provider, message, source_host) VALUES (\"' + str(timestamp) + '\",\"' + str(self.date) + '\",\"' + \
              str(self.time) + '\",\"' + str(fc.uptime) + '\",\"' + str(config["uplinks"][inc]["ip"]) + '\",\"' + \
              str(fc.external_ip) + '\",\"' + str(fc.external_ipv6) + '\",\"' + str(int(fc.is_linked)) + '\",\"' + \
              str(int(fc.is_connected)) + '\",\"' + str(fc.str_transmission_rate[0]) + '\",\"' + \
              str(fc.str_transmission_rate[1]) + '\",\"' + str(fc.str_max_bit_rate[0]) + '\",\"' + \
              str(fc.str_max_bit_rate[1]) + '\",\"' + str(fc.str_max_linked_bit_rate[0]) + '\",\"' + \
              str(fc.str_max_linked_bit_rate[1]) + '\",\"' + str(fc.modelname) + '\",\"' + \
              str(fc.fc.system_version) + '\",\"' + str(config["uplinks"][inc]["provider"]) + '\",\"' + self.status + '\",\"' + \
              socket.gethostname() + '\")'

        logger.debug(str(sql))
        with con.cursor() as cur:
            cur.execute(sql)
        con.commit()
        con.close()

    def run(self):
        while True:
            for i in range(len(self.config["uplinks"])):
                t = Thread(target=self.fetch_data, args=(self.config, i))
                t.start()
            time.sleep(self.config["interval"])
