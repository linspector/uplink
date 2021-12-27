# uplink - is not some program expecting uplinks to work!

## **This README file is not up-to-date! It will be fixed soon to explain the installation and the usage of uplink.**

uplink is a tool to monitor the uplink status of AVM FRITZ!Box Cable and DSL based routers. It uses the TR-064 protocol over UPnP.

## Features

For now, I can say that uplink can monitor the status of you FRITZ!Box uplinks. It can log to a file and writes results to a MariaDB/MySQL database. With some editing of the code you can you use SQLite too but this feature is not active at the moment. This will change in the future. I switched to MariaDB because I run uplink on a RaspberryPi and are evaluating results on my workstation. I am working on a Gtk+ frontend to generate statistics...

## Requirements

 - A Linux based operating system (I don't test any other OS's but Raspbian is fine and a good target)
 - Git (only for installing from Git repository)
 - Python3 (running for me using 3.7.3, 3.8.5, 3.9.7 and 3.10.1 on Linux) 
 - fritzconnection >= 1.5.0 (included as submodule in the Git repository)
 - pymysql >= 0.10.1
 - sqlalchemy = 1.4.27 (not for now)
 - urwid = 2.1.2 (not for now)

Just install the 3rd party dependencies using `pip install $PACKAGE` or your OS package manager
## Installation

    git clone https://git.unixpeople.org/hanez/uplink.git
    cd uplink
    # To get a local copy of fritzconnection you need to get the submodules:
    git submodule update --init --recursive
    cp config.example.json config.json

### Configuration

Edit config.json to your needs.

#### Variables

 - interval: The polling interval
 - uplinks: List of devices you want to poll
   - provider: Custom name of the uplink provider
   - ip: The IP of the router device
   - password: The password of the router device

#### Example

    {
    "interval": 60,
    "database_type": "mysql", (NOT USED)
    "database":  "uplink",
    "database_host": "127.0.0.1",
    "database_user": "USER",
    "database_password": "PASSWORD",
    "cron": false, (NOT USED)
    "daemon": false, (NOT USED)
        "uplinks": [
            { "provider": "Cable Provider", "ip": "192.168.0.1", "password": "1234" },
            { "provider": "DSL Provider", "ip": "192.168.1.1", "password": "1234" }
        ]
    }

### Create Database

    TODO

## Usage

    ./uplink [-c | -d | -f] ./config.json 

### Help

    ./uplink --help

   ```
   usage: uplink [-h] [-c | -d | -f] [-i INTERVAL] [--version] CONFIGFILE
   
   uplink is a tool to monitor the link status of AVM FRITZ!Box Cable and DSL based routers.
   
   positional arguments:
   CONFIGFILE            the configfile to use
   
   options:
   -h, --help            show this help message and exit
   -c, --cron            cron mode executes the script only once without loop (default: false)
   -d, --daemon          run as native daemon (default: false)
   -f, --foreground      run looped in foreground (default: false)
   -i INTERVAL, --interval INTERVAL
   poll interval in seconds. this overrides config file settings. (default: 60)
   --version             show program's version number and exit
   ```

## View collected data

I actually use "[DBeaver](https://dbeaver.io/)" for taking a look at the data uplink is collecting.

There will be a Gtk+ frontend to uplink at some time but this project is at a very early stage of development, so I want to write the collector first. Even support for other SQL databases is in planning in conjunction with the Gtk+ frontend. I use MariaDB only because I can move fast-forward.
