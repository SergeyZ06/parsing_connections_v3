-- ddl_query_0_0
-- This query creates tables 'clients' and 'connections'.

PRAGMA foreign_keys = 'off';

BEGIN TRANSACTION;-- Table: clients

CREATE TABLE IF NOT EXISTS clients (
    id_client        INTEGER PRIMARY KEY ASC AUTOINCREMENT
                             UNIQUE
                             NOT NULL,
    Process_ID       INT     NOT NULL,
    Source           VARCHAR NOT NULL,
    Source_port      INT     NOT NULL,
    Destination      VARCHAR NOT NULL,
    Destination_port INT     NOT NULL
);-- Table: connections

CREATE TABLE IF NOT EXISTS connections (
    id_connection   INTEGER  PRIMARY KEY AUTOINCREMENT
                             UNIQUE
                             NOT NULL,
    id_client       INTEGER  NOT NULL
                             REFERENCES clients (id_client),
    Throughput_KB_s REAL     NOT NULL,
    timestamp       DATETIME NOT NULL
                             DEFAULT (datetime('now', 'localtime') ),
    error           VARCHAR
);

COMMIT TRANSACTION ; 

PRAGMA foreign_keys = 'on';
