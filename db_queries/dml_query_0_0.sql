-- dml_query_0_0
-- This query records data into the table 'clients'.

INSERT INTO clients (
                        Process_ID,
                        Source,
                        Source_port,
                        Destination,
                        Destination_port
                    )
                    VALUES (
                        $VARIABLE_PROCESS_ID$,
                        '$VARIABLE_SOURCE$',
                        $VARIABLE_SOURCE_PORT$,
                        '$VARIABLE_DESTINATION$',
                        $VARIABLE_DESTINATION_PORT$
                    );
