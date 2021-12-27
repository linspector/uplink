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

import pymysql
import socket
import time
import calendar

try:
    from fritzconnection.fritzconnection.lib.fritzstatus import FritzStatus
except ImportError:
    from fritzconnection.lib.fritzstatus import FritzStatus

from threading import Thread
from uplink.daemon import Daemon


class Uplink(Daemon):

    def __init__(self, pid_file, config):
        self.pid_file = pid_file
        self.config = config

    @staticmethod
    def get_data(config, inc):
        try:
            # TODO: Think about using a DB ORM (SQLAlchemy?) to make this program supporting different databases like
            #  sqlite and Postgres
            con = pymysql.connect(host=config["database_host"],
                                  user=config["database_user"],
                                  password=config["database_password"],
                                  database=config["database"])
        except Exception as err:
            # TODO: Replace all lines like this with generic Python logging
            print(str("Uplink: Database connection failed: " + str(err)))
            exit(1)

        timestamp = calendar.timegm(time.gmtime())
        local_time = time.localtime(timestamp)
        d = time.strftime("%Y-%m-%d", local_time)
        t = time.strftime("%H:%M:%S", local_time)

        try:
            fc = FritzStatus(address=config["uplinks"][inc]["ip"], password=config["uplinks"][inc]["password"])
        except Exception as err:
            # TODO: Replace all lines like this with generic Python logging
            print(str(str(err) + " on device with ip: " + config["uplinks"][inc]["ip"]))
            # TODO: Fix to long lines and make the SQL statement more readable
            sql = 'INSERT INTO log (timestamp, date, time, internal_ip, is_linked, is_connected, provider, message, ' \
                  'source_host)  VALUES (\"' + str(timestamp) + '\",\"' + str(d) + '\",\"' + str(t) + '\",\"' + \
                  str(config["uplinks"][inc]["ip"]) + '\",\"' + "0" + '\",\"' + "0" + '\",\"' + \
                  str(config["uplinks"][inc]["provider"]) + '\",\"ERROR: ' + str(err) + '\",\"' + socket.gethostname() + \
                  '\")'

            # TODO: Replace all lines like this with generic Python logging
            # print(str(sql))
            with con.cursor() as cur:
                cur.execute(sql)
            con.commit()
            exit(1)

        if fc.is_connected:
            status = "UP"
        else:
            status = "DOWN"

        # TODO: Replace all lines like this with generic Python logging
        print(str("[" + str(d) + " " + str(t) + "] " +config["uplinks"][inc]["provider"] + " " + status))

        # TODO: Fix to long lines and make the SQL statement more readable
        sql = 'INSERT INTO log (timestamp, date, time, uptime, internal_ip, external_ip, external_ipv6, is_linked, ' \
              'is_connected, str_transmission_rate_up, str_transmission_rate_down, str_max_bit_rate_up, ' \
              'str_max_bit_rate_down, str_max_linked_bit_rate_up, str_max_linked_bit_rate_down, modelname, ' \
              'system_version, provider, message, source_host) VALUES (\"' + str(timestamp) + '\",\"' + str(d) + '\",\"' + \
              str(t) + '\",\"' + str(fc.uptime) + '\",\"' + str(config["uplinks"][inc]["ip"]) + '\",\"' + \
              str(fc.external_ip) + '\",\"' + str(fc.external_ipv6) + '\",\"' + str(int(fc.is_linked)) + '\",\"' + \
              str(int(fc.is_connected)) + '\",\"' + str(fc.str_transmission_rate[0]) + '\",\"' + \
              str(fc.str_transmission_rate[1]) + '\",\"' + str(fc.str_max_bit_rate[0]) + '\",\"' + \
              str(fc.str_max_bit_rate[1]) + '\",\"' + str(fc.str_max_linked_bit_rate[0]) + '\",\"' + \
              str(fc.str_max_linked_bit_rate[1]) + '\",\"' + str(fc.modelname) + '\",\"' + \
              str(fc.fc.system_version) + '\",\"' + str(config["uplinks"][inc]["provider"]) + '\",\"' + status + '\",\"' + \
              socket.gethostname() + '\")'

        # TODO: Replace all lines like this with generic Python logging
        # print(str(sql))
        with con.cursor() as cur:
            cur.execute(sql)
        con.commit()
        con.close()

    def get_config(self):
        return self.config

    def run(self):
        while True:
            for i in range(len(self.config["uplinks"])):
                t = Thread(target=self.get_data, args=(self.get_config(), i))
                t.start()
            if self.config["cron"]:
                break
            time.sleep(self.config["interval"])
