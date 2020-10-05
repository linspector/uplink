# uplink - is not some program expecting uplinks to work!

**THIS CODE IS AT A VERY EARLY STAGE OF DEVELOPMENT! USE AT YOUR OWN RISK!**

**SINCE THIS CODE CHANGES EVERY DAY THE DOCUMENTATION MAY NOT BE CORRECT!**

uplink is a tool to monitor the uplink status of AVM FRITZ!Box Cable and DSL based routers. It uses the TR-064 protocol over UPnP.

## Features

For now I can say that uplink can monitor the status of you FRITZ!Box uplinks. It can log to a file and writes results to a MariaDB/MySQL database. With some editing of the code you can you use SQLite too but this feature is not active at the moment. This will change in the future. I switched to MariaDB because I run uplink on a RaspberryPi and are evaluating results on my workstation. I am working on a Gtk+ frontend to generate statistics...

## Requirements

 - Git (only for installing from Git repository)
 - Python3 (running for me using 3.7.3 on Raspbian 10 and 3.8.5 on Arch Linux) 
 - fritzconnection >= 1.3.4
 - pymysql >= 0.10.1

Just install the 3rd party dependencies using `pip install $PACKAGE` or your OS package manager
## Installation

    git clone https://git.unixpeople.org/hanez/uplink.git
    cd uplink
    cp config.example.json config.json

### Configuration

Edit config.json to your needs.

#### Variables

 - interval: The polling interval
 - database: Path to sqlite3 Database
 - uplinks: List of devices you want to poll
   - provider: Custom name of the uplink provider
   - ip: The IP of the router device
   - password: The password of the router device

#### Example

    {
    "interval": 60,
    "database_type": "mysql",
    "database":  "uplink",
    "database_host": "127.0.0.1",
    "database_user": "USER",
    "database_password": "PASSWORD",
    "cron": false,
    "daemon": false,
        "uplinks": [
            { "provider": "Cable Provider", "ip": "192.168.0.1", "password": "1234" },
            { "provider": "DSL Provider", "ip": "192.168.1.1", "password": "1234" }
        ]
    }

### Create Database

    sqlite3 uplink.sqlite3 < uplink.sql

## Usage

    ./uplink ./config.json

### Help

    ./uplink --help

## View collected data

I actually use "[DBeaver](https://dbeaver.io/)" for taking a look at the data uplink is collecting.

There will be a Gtk+ frontend to uplink at some time but this project is at a very early stage of development, so I want to write the collector first. Even support for other SQL databases is in planning in conjunction with the Gtk+ frontend. I use MariaDB only because I can move fast-forward.

## TODO (in no particular order)

 - A lot... :)
 - Make all config vars as ARGS and vice versa. ARGS have higher priority. Chain: default -> config -> ARGS.
 - ~~Parallelize queries using threads to improve performance; Does not work using SQLite because of exclusive access to the database~~ **DONE**
 - ~~SQL server backend; MariaDB/MySQL?~~ **DONE**
 - Bring back SQLite support
 - Switch to ORM (peewee?) to support PostgreSQL, MySQL and SQLite.
 - Gtk+ frontend connecting to the database or loading a local copy of a SQLite file. wxGlade?
 - ~~A cron mode to not let uplink run in an endless loop to be scheduled and executed by cron.~~ **DONE**
 - A daemon mode to be a real UNIX daemon. For now, it's just sleep() based.
 - Always keep platform independence in mind but not if uplink looses nice features on Linux. 

