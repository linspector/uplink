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

#import gammu

from logging import getLogger

logger = getLogger(__name__)


class Notification:

    def __init__(self, configuration):
        self.__configuration = configuration
        #self.__state_machine = gammu.StateMachine()
        #self.__state_machine.ReadConfig(
        #    self.__configuration.get_notification_gammu_configuration())

    def send(self, status):
        #message = {
        #    "Number": self.__configuration.get_notification_gammu_receiver(),
        #    "Text": "message text",
        #    "SMSC": {"Location": 1},
        #}
        #self.__state_machine.SendSMS(message)
        logger.error(status)
