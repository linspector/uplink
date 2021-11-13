#!/usr/bin/python3 -d

"""
Daemon testing file... Daemons in Python are new to me because I only worked on CLI, Gtk+ and Django projects before.

Let's have some fun... :)
"""

from daemon import Daemon


class Test(Daemon):

    def __init__(self, pid_file, color, size):
        # super().__init__(pid_file)
        self.pid_file = pid_file
        self.color = color
        self.size = size

    def run(self):
        # Write my daemon test code here:
        return


Test = Test("/tmp/uplink.pid", "Red", "XXL")
Test.start()
