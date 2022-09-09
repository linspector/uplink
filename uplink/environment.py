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

import re
import socket

from logging import getLogger

logger = getLogger('uplink')

"""
This is experimental because you can set what you want but if a env key you set already exists it 
will be overwritten. But it is an easy and maybe secure way to to set runtime variables which should 
not affect the execution of uplink but may be required variables to execute to your wanted 
configuration. Core functionality must not be affected when using this class!
"""


class Environment:

    def __init__(self):
        # environment vars which can be set dynamically at runtime. these vars are shared across all
        # objects and readable and writable by all of them.
        self.__env = {}

    def get_env_var(self, key):
        if key in self.__env:
            return self.__env[key]
        else:
            logger.info('environment var "' + key + '" not found! could be that is set late at '
                                                    'runtime. if you encounter errors executing '
                                                    'uplink, something is wrong in the code. '
                                                    'please consider to report this as a bug! btw. '
                                                    'INFO is not an ERROR!')
            return False

    def set_env_var(self, key, value):
        self.__env[key] = value
