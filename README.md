# uplink - is not some program expecting uplinks to work!

**THIS CODE IS AT A VERY EARLY STAGE OF DEVELOPMENT! USE AT YOUR OWN RISK!**

uplink is a tool to monitor the uplink status of AVM FRITZ!Box Cable and DSL based routers. It uses the TR-064 protocol over UPnP.

## Features

TODO: Write feature list

## Requirements

 - Python >= 3.8
 - fritzconnection >= 1.3.4
   - https://pypi.org/project/fritzconnection/
 - peewee >= 3.13.3
   - https://pypi.org/project/peewee/
 - Git (Just to install the way I do. You can also install downloading a .zip file and install libraries by yourself... not what I like, so I actually will not take care of this.)

3rd party libraries are included as Git submodule. See installation instructions below. Actually I use the current repository code. This will change but for development this is the easiest solution. I will switch to stable releases some day.

## Installation

    git clone https://git.unixpeople.org/hanez/uplink.git
    cd uplink
    git submodule update --init --recursive
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
        "database":  "./uplink.sqlite3",
        "cron_mode": false,
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

I actually use "[DB Browser for SQLite](https://sqlitebrowser.org/)" for taking a look at the
data uplink is collecting.

There will be a Gtk+ frontend to uplink at some time but this project is at a very early
stage of development, so I want to write the collector first. Even support for other SQL
databases is in planning in conjunction with the Gtk+ frontend. I use sqlite3 only because I
can move fast-forward.

## TODO (in no particular order)

 - A lot... :)
 - Make all config vars as ARGS and vice versa. ARGS have higher priority. Chain: default -> config -> ARGS.
 - Parallelize queries using threads to improve performance; Does not work using SQLite because of exclusive access to the database
 - SQL server backend; PostgreSQL? Or peewee ORM to support PostgreSQL, MySQL and SQLite.
 - Gtk+ frontend. wxGlade?
 - ~~A cron mode to not let uplink run in an endless loop to be scheduled and executed by cron.~~
 - A daemon mode to be a real UNIX daemon. For now, it's just sleep() based.
 - Always keep platform independence in mind but not if uplink looses nice features on Linux. 

