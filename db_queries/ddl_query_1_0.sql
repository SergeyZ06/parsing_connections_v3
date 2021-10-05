-- ddl_query_1_0
-- This query creates table 'durations'.

PRAGMA foreign_keys = 'off';

BEGIN TRANSACTION;-- Table: durations

CREATE TABLE IF NOT EXISTS durations (
    id_duration      INTEGER  PRIMARY KEY AUTOINCREMENT
                              NOT NULL
                              UNIQUE,
    id_client        INTEGER  REFERENCES clients (id_client) 
                              NOT NULL,
    duration_seconds BIGINT   NOT NULL,
    timestamp_first  DATETIME NOT NULL,
    timestamp_last   DATETIME NOT NULL
);

COMMIT TRANSACTION ; 

PRAGMA foreign_keys = 'on';
