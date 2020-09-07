# UPLINK 0.1

TODO: Write description.

## Requirements

 - Python >= 3.8
 - fritzconnection >= 1.3.4 (Included as Git submodule. See installation instructions below)
   - https://pypi.org/project/fritzconnection/
   - https://fritzconnection.readthedocs.io/en/1.3.4/index.html

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