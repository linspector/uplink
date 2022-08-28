# Copyright (c) 2022 Johannes Findeisen <you@hanez.org>
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

from logging import getLogger

logger = getLogger(__name__)


class Model:

    def __init__(self, configuration):
        self.__configuration = configuration

        self.__date = None
        self.__external_ip = None
        self.__external_ipv6 = None
        # no set method for id; it is auto incrementing in the database
        self.__id = None
        self.__internal_ip = None
        self.__is_connected = None
        self.__is_linked = None
        # TODO: rename message to status
        self.__message = None
        self.__model_name = None
        self.__provider = None
        self.__source_host = None
        self.__str_max_bit_rate_down = None
        self.__str_max_bit_rate_up = None
        self.__str_max_linked_bit_rate_down = None
        self.__str_max_linked_bit_rate_up = None
        self.__str_transmission_rate_down = None
        self.__str_transmission_rate_up = None
        self.__system_version = None
        self.__time = None
        self.__timestamp = None
        self.__uptime = None

    # set methods:
    def set_date(self, date):
        self.__date = date

    def set_external_ip(self, external_ip):
        self.__external_ip = external_ip

    def set_external_ipv6(self, external_ipv6):
        self.__external_ipv6 = external_ipv6

    def set_internal_ip(self, internal_ip):
        self.__internal_ip = internal_ip

    def set_is_connected(self, is_connected):
        self.__is_connected = is_connected

    def set_is_linked(self, is_linked):
        self.__is_linked = is_linked

    def set_message(self, message):
        self.__message = message

    def set_model_name (self, model_name):
        self.__model_name = model_name

    def set_provider(self, provider):
        self.__provider = provider

    def set_source_host(self, source_host):
        self.__source_host = source_host

    def set_str_max_bit_rate_down(self, str_max_bit_rate_down):
        self.__str_max_bit_rate_down = str_max_bit_rate_down

    def set_str_max_bit_rate_up(self, str_max_bit_rate_up):
        self.__str_max_bit_rate_up = str_max_bit_rate_up

    def set_str_max_linked_bit_rate_down(self, str_max_linked_bit_rate_down):
        self.__str_max_linked_bit_rate_down = str_max_linked_bit_rate_down

    def set_str_max_linked_bit_rate_up(self, str_max_linked_bit_rate_up):
        self.__str_max_linked_bit_rate_up = str_max_linked_bit_rate_up

    def set_str_transmission_rate_down(self, str_transmission_rate_down):
        self.__str_transmission_rate_down = str_transmission_rate_down

    def set_str_transmission_rate_up(self, str_transmission_rate_up):
        self.__str_transmission_rate_up = str_transmission_rate_up

    def set_system_version(self, system_version):
        self.__system_version = system_version

    def set_time(self, time):
        self.__time = time

    def set_timestamp(self, timestamp):
        self.__timestamp = timestamp

    def set_uptime(self, uptime):
        self.__uptime = uptime

    # get methods:
    def get_date(self):
        return self.__date

    def get_external_ip(self):
        return self.__external_ip

    def get_external_ipv6(self):
        return self.__external_ipv6

    def get_id(self):
        return self.__id

    def get_internal_ip(self):
        return self.__internal_ip

    def get_is_connected(self):
        return self.__is_connected

    def get_is_linked(self):
        return self.__is_linked

    def get_message(self):
        return self.__message

    def get_model_name(self):
        return self.__model_name

    def get_provider(self):
        return self.__provider

    def get_source_host(self):
        return self.__source_host

    def get_str_max_bit_rate_down(self):
        return self.__str_max_bit_rate_down

    def get_str_max_bit_rate_up(self):
        return self.__str_max_bit_rate_up

    def get_str_max_linked_bit_rate_down(self):
        return self.__str_max_linked_bit_rate_down

    def get_str_max_linked_bit_rate_up(self):
        return self.__str_max_linked_bit_rate_up

    def get_str_transmission_rate_down(self):
        return self.__str_transmission_rate_down

    def get_str_transmission_rate_up(self):
        return self.__str_transmission_rate_up

    def get_system_version(self):
        return self.__system_version

    def get_time(self):
        return self.__time

    def get_timestamp(self):
        return self.__timestamp

    def get_uptime(self):
        return self.__uptime
