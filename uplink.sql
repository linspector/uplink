CREATE TABLE "log" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"datetime"	TEXT NOT NULL,
	"uptime"	INTEGER,
	"external_ip"	TEXT,
	"external_ipv6"	TEXT,
	"is_linked"	INTEGER,
	"is_connected"	INTEGER,
	"str_transmission_rate_up"	TEXT,
	"str_transmission_rate_down"	TEXT,
	"str_max_bit_rate_up"	TEXT,
	"str_max_bit_rate_down"	TEXT,
	"str_max_linked_bit_rate_up"	TEXT,
	"str_max_linked_bit_rate_down"	TEXT,
	"modelname"	TEXT,
	"system_version"	TEXT
);