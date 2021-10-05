-- dml_query_0_1
-- This query records data into the table 'connections'.

INSERT INTO connections (
                            id_client,
                            Throughput_KB_s,
                            timestamp,
                            error
                        )
                        VALUES (
                            $VARIABLE_ID_CLIENT$,
                            $VARIABLE_THROUGHPUT_KB_S$,
                            '$TIMESTAMP$',
                            $ERROR$
                        );
