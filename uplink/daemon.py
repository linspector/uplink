"""
Generic linux daemon base class for python 3.x.

Original Source:
https://web.archive.org/web/20131017130434/http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
https://web.archive.org/web/20131017130434/http://www.jejik.com/files/examples/daemon3x.py
See daemon3x.py in the uplink source tree.

More Information:
https://franklingu.github.io/programming/2016/03/01/creating-daemon-process-python-example-explanation/
https://dpbl.wordpress.com/2017/02/12/a-tutorial-on-python-daemon/
"""

from logging import getLogger
import sys
import os
import time
import atexit
import signal

logger = getLogger(__name__)


# TODO: Check why pid files are not being deleted when sending the TERM signal
class Daemon:
    """
    A generic daemon class.

    Usage: subclass the daemon class and override the run() method.
    """

    def __init__(self, pid_file):
        self.pid_file = pid_file

    def daemonize(self):
        """
        Deamonize class. UNIX double fork mechanism.
        """

        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as err:
            logger.error('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)

        # decouple from parent environme
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as err:
            logger.error('fork #2 failed: {0}\n'.format(err))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.del_pid)

        pid = str(os.getpid())
        with open(self.pid_file, 'w+') as f:
            f.write(pid + '\n')

    def del_pid(self):
        os.remove(self.pid_file)

    def start(self):
        """
        Start the daemon.
        """

        # Check for a pidfile to see if the daemon already runs
        try:
            with open(self.pid_file, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            message = "pid_file {0} already exist. Daemon already running?\n"
            logger.error(message.format(self.pid_file))
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon.
        """

        # Get the pid from the pidfile
        try:
            with open(self.pid_file, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = "pid_file {0} does not exist. Daemon not running?\n"
            logger.error(message.format(self.pid_file))
            # not an error in a restart
            return

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pid_file):
                    os.remove(self.pid_file)
            else:
                logger.error(str(err.args))
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon.
        """
        self.stop()
        self.start()

    def run(self):
        """
        Override this method when you subclass Daemon.
        It will be called after the process has been daemonized by
        start() or restart().
        """
