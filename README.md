# uplink -is a tool to monitor the uplink status of AVM FRITZ!Box Cable and DSL based routers.

## About

uplink is a tool to monitor the uplink status of AVM FRITZ!Box Cable and DSL based routers. It uses the
<a href="https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AVM_TR-064_first_steps.pdf"
class="ext">TR-064 protocol</a> over UPnP (I think it is only used by AVM in Germany).

*This site is related to version 0.8 of uplink (current version: 0.8.3.2).*

## Features

For now, I can say that uplink can monitor the status of you FRITZ!Box uplinks. It can log to a file and
writes results to a MariaDB/MySQL database. With some editing of the code you can you use SQLite too but this feature
is not active at the moment. This will change in the future. I switched to MariaDB because I run uplink on a
RaspberryPi and are evaluating results on my workstation. I am working on a Gtk+ frontend to generate statistics...

## Requirements

### Basic tools

 - A Linux based operating system (I don't test any other OS's but Linux and Raspbian is fine and a good target)
 - Git (only for installing from Git repository)
 - Python3 (running for me using 3.7.3, 3.8.5, 3.9.7 and 3.10.6 on Linux)

### Python libraries

 - fritzconnection >= 1.5.0
 - pymysql >= 0.10.1

Just install 3rd party Python libraries using "pip":

<pre class="clean language-plaintext">pip install $PACKAGE</pre>

Maybe the package is available in your OS package manager, then install it from there or set up a virtual environment!

## Installation

<pre class="clean language-plaintext">cd
git clone https://github.com/linspector/uplink.git
cd uplink</pre>

### Create Database

For now there is only the file uplink.sql which will create the tables in your MariaDB/MySQL database.

The file is under ./files/uplink.sql

## Configuration

Edit ./etc/config.json to your needs.

### Example

This example contains comments which will make the JSON file broken when copying and pasting, so it is only for
showing the features of uplink. Use the example in ./etc/ or remove the comments when you want to run uplink without
errors.

<pre class="code language-json">{
    "database_host": "127.0.0.1",
    "database_name": "uplink",
    "database_password": "PASSWORD",
    "database_port": 3306, (OPTIONAL)
    "database_type": "mariadb", (CURRENTLY NOT IN USE)
    "database_user": "uplink",
    "notification_gammu": true, (OPTIONAL)
    "notification_gammu_configuration": "~/uplink/etc/gammurc", (OPTIONAL)
    "notification_gammu_receiver": "+4900000000",
    "httpserver": true, (OPTIONAL)
    "httpserver_host": "127.0.0.1", (OPTIONAL)
    "httpserver_port": 1042, (OPTIONAL)
    "interval": 60, (OPTIONAL)
    "log_file": "~/uplink/log/uplink.log", (OPTIONAL)
    "log_level": "verbose", (OPTIONAL)
    "log_count": 5, (OPTIONAL)
    "log_size": 10485760, (OPTIONAL)
    "pid_file": "/var/run/user/1000/uplink.pid", (OPTIONAL)
    "run_mode": "cron", (NOT IN USE)
    "speedtest": true, (OPTIONAL)
    "speedtest_interval": 3600, (OPTIONAL)
    "speedtest_url": "https://unixpeople.org/uplink.test", (OPTIONAL)
    "uplinks": [
        {
            "identifier": "cable",
            "primary": true, (OPTIONAL, CURRENTLY NOT IN USE)
            "ip": "192.168.0.1",,
            "password": "PASSWORD",
            "provider": "Cable Provider" (OPTIONAL)
        },
        {
            "identifier": "dsl",
            "ip": "192.168.1.1",
            "password": "PASSWORD",
            "provider": "DSL Provider" (OPTIONAL)
        }
    ]
}</pre>

<p>Some optional values are set to default values in the sourcecode. You can find them at the top of
./uplink/configuration.py in the root of the uplink source diretory.</p>

<p>A configuration file without comments is found at ./etc/uplink.json.example. Just execute the following command and
edit etc/config.json.</p>

<pre class="clean language-plaintext">cp ./etc/config.json.example ./etc/config.json</pre>

## Usage

<pre class="clean language-bash">PYTHONPATH=$(pwd) ./bin/uplink [-c | -d | -f] ./etc/config.json</pre>

You need at least set -c, -d or -f as the run mode (there is no default) and a valid configuration file to make it
possible to run uplink.

### Help

<pre class="clean language-bash">PYTHONPATH=$(pwd) ./bin/uplink --help</pre>

<pre class="clean language-plaintext">usage: uplink [-h] [-c] [-d] [-k] [-r] [-f] [--httpserver] [-i INTERVAL] [-l LOGFILE] [-s]
              [--version]
              CONFIGFILE

uplink is a tool to monitor the link status of AVM FRITZ!Box Cable and DSL based routers.

positional arguments:
  CONFIGFILE            the configuration file to use

options:
  -h, --help            show this help message and exit
  -c, --cron            cron mode executes the script only once without loop (default: false)
  -d, --daemon          run as native daemon (default: false)
  -k, --kill            kill the daemon if it is running (default: false)
  -r, --restart         restart the daemon if it is running(default: false)
  -f, --foreground      run looped in foreground (default: false)
  --httpserver          enable the http server for status information and statistics
  -i INTERVAL, --interval INTERVAL
                        poll interval in seconds. this overrides config file settings (default:
                        60)
  -l LOGFILE, --logfile LOGFILE
                        logfile to use. this overrides config file settings
  -s, --stdout          log to stdout
  --version             show program's version number and exit

uplink is not some program expecting uplinks to work!
</pre>

## View collected data

I actually use "[DBeaver](https://dbeaver.io/)" for taking a look at the data uplink is collecting.

There will be a Gtk+ frontend to uplink at some time but this project is at a very early stage of development,
so I wanted to write the collector first. Even support for other SQL databases is planned in conjunction with a
Gtk+ frontend. I use MariaDB because I can move on fast-forward.

## Planned features

- A lot... :)
- Make all config vars as ARGS and vice versa. ARGS have higher priority. Chain: default -> config -> ARGS.
- Bring back SQLite support.
- Switch to ORM (peewee, sqlalchemy?) to support PostgreSQL, MariaDB/MySQL, SQLite and maybe more databases.
- Gtk+/urwid frontend for visualizing the collected data. wxGlade?
- A tool to generate reports for showing to your uplink provider.
- Always keep platform independence in mind but not if uplink looses nice features on Linux.
- Implement a speedtest feature to regularly run speedtest but independent to uptime checks with different interval.
- A small embedded webserver to view what is going on.

## License

uplink is licensed under the terms of the MIT License.

<pre class="clean language-plaintext">Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice (including the next
paragraph) shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</pre>
