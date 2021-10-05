-- ddl_query_2_1
-- This query recreates tables 'loads' and 'clients_in_loads'.

PRAGMA foreign_keys = 'off';

BEGIN TRANSACTION;-- Table: loads

DROP TABLE IF EXISTS loads;

CREATE TABLE IF NOT EXISTS loads (
    id_load             INTEGER  PRIMARY KEY AUTOINCREMENT
                                 UNIQUE
                                 NOT NULL,
    count_clients       INT      NOT NULL,
    timestamp_first     DATETIME NOT NULL,
    timestamp_last      DATETIME NOT NULL,
    avg_Throughput_KB_s REAL     NOT NULL,
    max_Throughput_KB_s REAL     NOT NULL
);-- Table: clients_in_loads

DROP TABLE IF EXISTS clients_in_loads;

CREATE TABLE IF NOT EXISTS clients_in_loads (
    id_client_in_load   INTEGER PRIMARY KEY AUTOINCREMENT
                                UNIQUE,
    id_load             INTEGER REFERENCES loads (id_load) 
                                NOT NULL,
    id_client           INTEGER REFERENCES clients (id_client) 
                                NOT NULL,
    avg_Throughput_KB_s REAL    NOT NULL,
    max_Throughput_KB_s REAL    NOT NULL
);

COMMIT TRANSACTION ; 

PRAGMA foreign_keys = 'on';
