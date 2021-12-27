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
import json
import logging
import logging.handlers
import os
import sys
import time

from threading import Thread
from uplink.uplink import Uplink

# Version format: MAJOR.FEATURE.FIXES
__version__ = "0.5.0-development"

# TODO: CHECK ALL ERROR HANDLING!!!
# TODO: IDEA: Implement a small webserver inline to get statistics and graphs over the network? Or maybe better as a
#  separate daemon
# TODO: Make use of more args passed to the script
# TODO: Implement a speedtest that will also run regularly but in an individual interval

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description="uplink is a tool to monitor the link status of AVM FRITZ!Box Cable and DSL "
                    "based routers.",
        epilog="uplink is not some program expecting uplinks to work!",
        prog="uplink")

    parser.add_argument("config", metavar="CONFIGFILE", help="the configfile to use")

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-c", "--cron", default=False, dest="cron", action="store_true",
                      help="cron mode executes the script only once without loop (default: false)")

    mode.add_argument("-d", "--daemon", default=False, dest="daemon", action="store_true",
                      help="run as native daemon (default: false)")

    mode.add_argument("-f", "--foreground", default=False, dest="foreground", action="store_true",
                      help="run looped in foreground (default: false)")

    parser.add_argument("-i", "--interval", type=int, help="poll interval in seconds. this "
                                                           "overrides config file settings. "
                                                           "(default: 60)")

    """
    parser.add_argument("-b", "--database", metavar="DATABASE", help="database to use")

    parser.add_argument("-u", "--user", type=str, help="database username")

    parser.add_argument("-p", "--password", type=str, help="database password")
    """
    parser.add_argument("-l", "--logfile", metavar="FILE", help="logfile to use")

    parser.add_argument("-n", "--logcount", default=5, type=int,
                        help="maximum number of logfiles in rotation (default: 5)")

    parser.add_argument("-m", "--logsize", default=10485760, type=int,
                        help="maximum logfile size in bytes (default: 10485760)")

    parser.add_argument("-s", "--stdout", default=False, dest="stdout", action="store_true",
                        help="log to stdout")

    output = parser.add_mutually_exclusive_group()
    output.add_argument("-q", "--quiet", action="store_const", dest="loglevel",
                        const=logging.ERROR, help="output only errors")

    output.add_argument("-w", "--warning", action="store_const", dest="loglevel",
                        const=logging.WARNING, help="output warnings")

    output.add_argument("-v", "--verbose", action="store_const", dest="loglevel",
                        const=logging.INFO, help="output info messages")

    output.add_argument("-e", "--debug", action="store_const", dest="loglevel",
                        const=logging.DEBUG, help="output debug messages")
    output.set_defaults(loglevel=logging.ERROR)

    parser.add_argument("--version", action="version", version="%(prog)s " + str(__version__))

    return parser.parse_args()


def main():
    args = parse_args()

    root_logger = logging.getLogger()

    if args.logfile:
        logfile = os.path.expanduser(args.logfile)
        if not os.path.exists(os.path.dirname(logfile)):
            os.makedirs(os.path.dirname(logfile))

        formatter1 = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
        handler1 = logging.handlers.RotatingFileHandler(args.logfile, maxBytes=args.logsize,
                                                        backupCount=args.logcount)
        handler1.setFormatter(formatter1)
        root_logger.addHandler(handler1)

    if args.stdout:
        formatter2 = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
        handler2 = logging.StreamHandler(sys.stdout)
        handler2.setFormatter(formatter2)
        root_logger.addHandler(handler2)

    root_logger.setLevel(args.loglevel)

    # TODO: Cleanup config.json and only define what really is needed
    config_path = args.config
    try:
        with open(config_path, 'r', encoding='utf-8') as configfile:
            config_data = configfile.read()
        config = json.loads(config_data)
    except Exception as err:
        logger.error(str("uplink: configuration error! " + str(err)))
        sys.exit(1)

    try:
        config["interval"]
    except KeyError:
        # interval not configured in configuration; using default value
        config["interval"] = 60

    if args.interval:
        # interval set in args is overriding configuration and default
        config["interval"] = args.interval

    uplink = Uplink("/tmp/uplink.pid", config)

    if args.cron:
        for i in range(len(config["uplinks"])):
            t = Thread(target=uplink.fetch_data, args=(config, i))
            t.start()
    elif args.daemon:
        uplink.start()
    elif args.foreground:
        while True:
            for i in range(len(config["uplinks"])):
                t = Thread(target=uplink.fetch_data, args=(config, i))
                t.start()
            try:
                time.sleep(config["interval"])
            except KeyboardInterrupt as err:
                logger.info(str("uplink: program terminated by user!"))
                sys.exit(0)
    else:
        logger.error("uplink: no run mode selected; use --cron (-c), --daemon (-d) or "
                     "--foreground (-f) to run uplink. use --help for more information")


if __name__ == "__main__":
    main()
