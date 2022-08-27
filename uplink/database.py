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

import calendar
import pymysql
import socket
import time

from logging import getLogger
from sqlalchemy import create_engine

logger = getLogger(__name__)


class Database:

    def __init__(self, configuration):
        self.configuration = configuration
        self.date = None
        self.time = None
        self.status = None

    def write_to_db(self, fc, ip, provider, status):
        timestamp = calendar.timegm(time.gmtime())
        local_time = time.localtime(timestamp)
        self.date = time.strftime('%Y-%m-%d', local_time)
        self.time = time.strftime('%H:%M:%S', local_time)

        try:
            con = pymysql.connect(host=self.configuration.get_database_host(),
                                  user=self.configuration.get_database_user(),
                                  password=self.configuration.get_database_password(),
                                  database=self.configuration.get_database_name())

            sql = 'INSERT INTO log (timestamp, date, time, uptime, internal_ip, external_ip, external_ipv6, is_linked, ' \
                  'is_connected, str_transmission_rate_up, str_transmission_rate_down, str_max_bit_rate_up, ' \
                  'str_max_bit_rate_down, str_max_linked_bit_rate_up, str_max_linked_bit_rate_down, modelname, ' \
                  'system_version, provider, message, source_host) VALUES (\"' + str(timestamp) + '\",\"' + str(self.date) + '\",\"' + \
                  str(self.time) + '\",\"' + str(fc.connection_uptime) + '\",\"' + str(ip) + '\",\"' + \
                  str(fc.external_ip) + '\",\"' + str(fc.external_ipv6) + '\",\"' + str(int(fc.is_linked)) + '\",\"' + \
                  str(int(fc.is_connected)) + '\",\"' + str(fc.str_transmission_rate[0]) + '\",\"' + \
                  str(fc.str_transmission_rate[1]) + '\",\"' + str(fc.str_max_bit_rate[0]) + '\",\"' + \
                  str(fc.str_max_bit_rate[1]) + '\",\"' + str(fc.str_max_linked_bit_rate[0]) + '\",\"' + \
                  str(fc.str_max_linked_bit_rate[1]) + '\",\"' + str(fc.modelname) + '\",\"' + \
                  str(fc.fc.system_version) + '\",\"' + str(provider) + '\",\"' + str(status) + '\",\"' + \
                  socket.gethostname() + '\")'

            with con.cursor() as cur:
                cur.execute(sql)
                con.commit()
                con.close()

        except Exception as err:
            logger.error(str("database connection failed: {0}".format(err)))
        return
