#!/usr/bin/python3 -d

import calendar
import datetime
# import daemon
import json
import sqlite3
import time

from fritzconnection.lib.fritzstatus import FritzStatus


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
        print(str(datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')) + " - " +
              config["uplinks"][i]["provider"] + ": " + status)
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
        # print(sql)
        c.execute(sql)
        print("##########################################################")
        conn.commit()
    conn.close()


def run(config):
    # with daemon.DaemonContext():
    while True:
        get_data(config)
        time.sleep(config["interval"])


if __name__ == "__main__":
    with open('config.json', 'r') as configfile:
        config_data = configfile.read()
    _config = json.loads(config_data)
    run(_config)
