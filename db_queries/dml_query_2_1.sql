-- dml_query_2_1
-- This query records data into the table 'clients_in_loads'.

INSERT INTO clients_in_loads (
                                 id_load,
                                 id_client,
                                 avg_Throughput_KB_s,
                                 max_Throughput_KB_s
                             )
                             VALUES (
                                 $VARIABLE_ID_LOAD$,
                                 $VARIABLE_ID_CLIENT$,
                                 $VARIABLE_AVG_THROUGHPUT_KB_S$,
                                 $VARIABLE_MAX_THROUGHPUT_KB_S$
                             );
