# TODO (in no particular order)

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
