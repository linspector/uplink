#!/usr/bin/python3 -d

# Copyright (c) 2020 Johannes Findeisen <you@hanez.org>
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

import argparse
import calendar
import datetime
# import daemon
import json
import logging
import logging.handlers
import os
import os.path as path
import sqlite3
import time

from fritzconnection.lib.fritzstatus import FritzStatus

__version__ = "0.1"

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description="uplink.",
        epilog="uplink is not some program expecting uplinks to work!",
        prog="uplink")

    parser.add_argument("--version", action="version", version="%(prog)s " + str(__version__))

    parser.add_argument("config", metavar="CONFIGFILE",
                        help="the configfile to use")

    parser.add_argument("-n", "--nocolor",
                        help="disable colored output")

    parser.add_argument("-l", "--logfile", default="./log/uplink.log", metavar="FILE",
                        help="set logfile to use (default: ./log/uplink.log)")

    parser.add_argument("-c", "--logcount", default=5, type=int,
                        help="maximum number of logfiles in rotation (default: 5)")

    parser.add_argument("-m", "--logsize", default=10485760, type=int,
                        help="maximum logfile size in bytes (default: 10485760)")

    output = parser.add_mutually_exclusive_group()
    output.add_argument("-q", "--quiet", action="store_const", dest="loglevel", const=logging.ERROR,
                        help="output only errors")

    output.add_argument("-w", "--warning", action="store_const", dest="loglevel", const=logging.WARNING,
                        help="output warnings")

    output.add_argument("-v", "--verbose", action="store_const", dest="loglevel", const=logging.INFO,
                        help="output info messages")

    output.add_argument("-d", "--debug", action="store_const", dest="loglevel", const=logging.DEBUG,
                        help="output debug messages")
    output.set_defaults(loglevel=logging.INFO)
    return parser.parse_args()


def get_data(config):
    conn = sqlite3.connect(config["database"])
    c = conn.cursor()
    for i in range(len(config["uplinks"])):
        timestamp = calendar.timegm(time.gmtime())
        fc = FritzStatus(address=config["uplinks"][i]["ip"], password=config["uplinks"][i]["password"])
        if fc.is_connected:
            status = "UP"
        else:
            status = "DOWN"

        logger.info(config["uplinks"][i]["provider"] + ": " + status)
        sql = 'INSERT INTO log (datetime, uptime, external_ip, external_ipv6,is_linked,is_connected, ' \
              'str_transmission_rate_up, str_transmission_rate_down, str_max_bit_rate_up, str_max_bit_rate_down, ' \
              'str_max_linked_bit_rate_up, str_max_linked_bit_rate_down, modelname, system_version) VALUES (\"' + \
              str(timestamp) + '\",\"' + str(fc.uptime) + '\",\"' + str(fc.external_ip) + '\",\"' + \
              str(fc.external_ipv6) + '\",\"' + str(int(fc.is_linked)) + '\",\"' + \
              str(int(fc.is_connected)) + '\",\"' + str(fc.str_transmission_rate[0]) + '\",\"' + \
              str(fc.str_transmission_rate[1]) + '\",\"' + str(fc.str_max_bit_rate[0]) + '\",\"' + \
              str(fc.str_max_bit_rate[1]) + '\",\"' + str(fc.str_max_linked_bit_rate[0]) + '\",\"' + \
              str(fc.str_max_linked_bit_rate[1]) + '\",\"' + str(fc.modelname) + '\",\"' + \
              str(fc.fc.system_version) + '\")'
        logging.debug(sql)
        c.execute(sql)
        conn.commit()
    conn.close()


def run(config):
    # with daemon.DaemonContext():
    while True:
        get_data(config)
        time.sleep(config["interval"])


if __name__ == "__main__":
    args = parse_args()

    configpath = args.config

    with open(configpath, 'r') as configfile:
        config_data = configfile.read()
    _config = json.loads(config_data)

    logfile = path.expanduser(args.logfile)
    if not path.exists(path.dirname(logfile)):
        os.makedirs(path.dirname(logfile))

    root_logger = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    handler = logging.handlers.RotatingFileHandler(args.logfile, maxBytes=args.logsize, backupCount=args.logcount)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(args.loglevel)

    run(_config)
