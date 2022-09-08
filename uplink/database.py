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

import pymysql

from logging import getLogger

logger = getLogger('uplink')


class Database:

    def __init__(self, configuration):
        self.__configuration = configuration

    def write_log_to_db(self, model):
        try:
            con = pymysql.connect(host=self.__configuration.get_database_host(),
                                  database=self.__configuration.get_database_name(),
                                  password=self.__configuration.get_database_password(),
                                  port=self.__configuration.get_database_port(),
                                  user=self.__configuration.get_database_user())

            sql = 'INSERT INTO log (' \
                  'timestamp, ' \
                  'date, ' \
                  'time, ' \
                  'uptime, ' \
                  'internal_ip, ' \
                  'external_ip, ' \
                  'external_ipv6, ' \
                  'is_linked, ' \
                  'is_connected, ' \
                  'str_transmission_rate_up, ' \
                  'str_transmission_rate_down, ' \
                  'str_max_bit_rate_up, ' \
                  'str_max_bit_rate_down, ' \
                  'str_max_linked_bit_rate_up, ' \
                  'str_max_linked_bit_rate_down, ' \
                  'model_name, ' \
                  'system_version, ' \
                  'provider, ' \
                  'message, ' \
                  'source_host ' \
                  ') VALUES (\"' + \
                  str(model.get_timestamp()) + '\",\"' + \
                  str(model.get_date()) + '\",\"' + \
                  str(model.get_time()) + '\",\"' + \
                  str(model.get_uptime()) + '\",\"' + \
                  str(model.get_internal_ip()) + '\",\"' + \
                  str(model.get_external_ip()) + '\",\"' + \
                  str(model.get_external_ipv6()) + '\",\"' + \
                  str(int(model.get_is_linked())) + '\",\"' + \
                  str(int(model.get_is_connected())) + '\",\"' + \
                  str(model.get_str_transmission_rate_up()) + '\",\"' + \
                  str(model.get_str_transmission_rate_down()) + '\",\"' + \
                  str(model.get_str_max_bit_rate_up()) + '\",\"' + \
                  str(model.get_str_max_bit_rate_down()) + '\",\"' + \
                  str(model.get_str_max_linked_bit_rate_up()) + '\",\"' + \
                  str(model.get_str_max_linked_bit_rate_down()) + '\",\"' + \
                  str(model.get_model_name()) + '\",\"' + \
                  str(model.get_system_version()) + '\",\"' + \
                  str(model.get_provider()) + '\",\"' + \
                  str(model.get_message()) + '\",\"' + \
                  str(model.get_source_host()) + '\")'

            with con.cursor() as cur:
                cur.execute(sql)
                con.commit()
                con.close()

        except Exception as err:
            logger.error(str("database connection failed: {0}".format(err)))
        return
