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

logger = getLogger('uplink')

"""
this is for environment vars which can be set dynamically at runtime. these vars are shared across
all objects and are readable and writable by all of them. environment variables are set at runtime
and currently not stored in the database. the goal is to minimize all of these vars but for now it
is nice feature to save states without saving them for runtime execution at another place.

this is experimental because you can set what you want but if a env key you set already exists it
will be overwritten. But it is an easy and maybe secure way to to set runtime variables which should
not affect the execution of uplink but may be required variables to execute to your wanted
configuration. Core functionality must not be affected when using this class!
"""


class Environment:

    def __init__(self):
        self.__env = {}

    def get_env_var(self, key):
        if key in self.__env:
            return self.__env[key]
        else:
            logger.info('environment var "' + key + '" not found! could be that it is set later at '
                                                    'runtime. if you encounter any errors '
                                                    'executing uplink, something is wrong in the '
                                                    'logic of the code. please consider reporting '
                                                    'this as a bug! btw. INFO is not an ERROR! ' 
                                                    'uplink should work even with missing '
                                                    'environment variables.')
            return False

    def set_env_var(self, key, value):
        self.__env[key] = value
