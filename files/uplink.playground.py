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
import json
import logging
import logging.handlers
import pymysql
import socket
import time

try:
    from fritzconnection.fritzconnection.lib.fritzstatus import FritzStatus
except ImportError:
    from fritzconnection.lib.fritzstatus import FritzStatus

from threading import Thread
from uplink.daemon import Daemon

# Version format: MAJOR.FEATURE.FIXES
__version__ = "0.3.0"

# logger = logging.getLogger(__name__)

# PURPLE = "\033[95m"
# BLUE = "\033[94m"
# YELLOW = "\033[93m"
# GRAY = "\033[90m"
# END = "\033[0m"


class Uplink(Daemon):

    def __init__(self, pid_file, config):
        self.pid_file = pid_file
        self.config = config

    @staticmethod
    def get_data(config, inc):
        try:
            con = pymysql.connect(host=config["database_host"],
                                  user=config["database_user"],
                                  password=config["database_password"],
                                  database=config["database"])
        except Exception as err:
            # logger.error("Database connection failed: " + str(err))
            print(str("Uplink: Database connection failed: " + str(err)))
            exit(1)

        timestamp = calendar.timegm(time.gmtime())
        local_time = time.localtime(timestamp)
        d = time.strftime("%Y-%m-%d ", local_time)
        t = time.strftime("%H:%M:%S", local_time)

        try:
            fc = FritzStatus(address=config["uplinks"][inc]["ip"], password=config["uplinks"][inc]["password"])
        except Exception as err:
            # logger.error(str(err) + " on device with ip: " + config["uplinks"][inc]["ip"])
            print(str(str(err) + " on device with ip: " + config["uplinks"][inc]["ip"]))
            sql = 'INSERT INTO log (timestamp, date, time, internal_ip, is_linked, is_connected, provider, message, ' \
                  'source_host)  VALUES (\"' + str(timestamp) + '\",\"' + str(d) + '\",\"' + str(t) + '\",\"' + \
                  str(config["uplinks"][inc]["ip"]) + '\",\"' + "0" + '\",\"' + "0" + '\",\"' + \
                  str(config["uplinks"][inc]["provider"]) + '\",\"ERROR: ' + str(err) + '\",\"' + socket.gethostname() + \
                  '\")'
            # logger.debug(sql)
            print(str(sql))
            with con.cursor() as cur:
                cur.execute(sql)
            con.commit()
            exit(1)

        if fc.is_connected:
            status = "UP"
        else:
            status = "DOWN"

        # logger.info(config["uplinks"][inc]["provider"] + " " + status)
        print(str(config["uplinks"][inc]["provider"] + " " + status))

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
        # logger.debug(sql)
        print(str(sql))
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


def parse_args():
    parser = argparse.ArgumentParser(
        description="uplink is a tool to monitor the link status of AVM FRITZ!Box Cable and DSL based routers.",
        epilog="uplink is not some program expecting uplinks to work!",
        prog="uplink")

    parser.add_argument("config", metavar="CONFIGFILE", help="the configfile to use")

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--cron", default=False, dest="cron", action="store_true",
                      help="cron mode executes the script only once without loop (default: false)")

    mode.add_argument("--daemon", default=False, dest="daemon", action="store_true",
                      help="run as native daemon (default: false)")

    mode.add_argument("--foreground", default=True, dest="foreground", action="store_true",
                      help="run in foreground (default: true)")

    parser.add_argument("-i", "--interval", default=60, type=int,
                        help="seconds poll interval (default: 60)")

    parser.add_argument("-b", "--database", metavar="DATABASE", help="database to use")

    parser.add_argument("-u", "--user", type=str, help="database username")

    parser.add_argument("-p", "--password", type=str, help="database password")

    parser.add_argument("-l", "--logfile", metavar="FILE", help="logfile to use")

    parser.add_argument("-c", "--logcount", default=5, type=int,
                        help="maximum number of logfiles in rotation (default: 5)")

    parser.add_argument("-m", "--logsize", default=10485760, type=int,
                        help="maximum logfile size in bytes (default: 10485760)")

    parser.add_argument("-s", "--stdout", default=False, dest="stdout", action="store_true", help="log to stdout")

    output = parser.add_mutually_exclusive_group()
    output.add_argument("-q", "--quiet", action="store_const", dest="loglevel", const=logging.ERROR,
                        help="output only errors")

    output.add_argument("-w", "--warning", action="store_const", dest="loglevel", const=logging.WARNING,
                        help="output warnings")

    output.add_argument("-v", "--verbose", action="store_const", dest="loglevel", const=logging.INFO,
                        help="output info messages")

    output.add_argument("-d", "--debug", action="store_const", dest="loglevel", const=logging.DEBUG,
                        help="output debug messages")
    output.set_defaults(loglevel=logging.ERROR)

    parser.add_argument("--version", action="version", version="%(prog)s " + str(__version__))

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # root_logger = logging.getLogger()

    # if args.stdout:
    #     formatter = logging.Formatter(
    #         PURPLE + "%(asctime)s" + END + ":" + BLUE + "%(levelname)s" + END + ":" + YELLOW + "%(name)s" + END + ":" + GRAY + "%(message)s" + END)
    #     handler1 = logging.StreamHandler(sys.stdout)
    #     handler1.setFormatter(formatter)
    #     root_logger.addHandler(handler1)

    # if args.logfile:
    #     logfile = path.expanduser(args.logfile)
    #     if not path.exists(path.dirname(logfile)):
    #         os.makedirs(path.dirname(logfile))
    #     formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    #     handler2 = logging.handlers.RotatingFileHandler(args.logfile, maxBytes=args.logsize, backupCount=args.logcount)
    #     handler2.setFormatter(formatter)
    #     root_logger.addHandler(handler2)

    # root_logger.setLevel(args.loglevel)

    config_path = args.config
    try:
        with open(config_path, 'r') as configfile:
            config_data = configfile.read()
        _config = json.loads(config_data)
    except Exception as err:
        # logger.error("Reading configuration file '" + config_path + "' failed: " + str(err))
        print(str("Uplink: Configuration Error!"))
        exit(1)

    # try:
    #     run(_config)
    # except KeyboardInterrupt:
    #     logger.info("Program terminated!")
    #     exit(0)

    Uplink = Uplink("/tmp/uplink.pid", _config)
    Uplink.start()
