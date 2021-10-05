-- sql_query_2_4
-- This query provides information from the table 'clients_in_loads':

SELECT c.id_client_in_load
  FROM clients_in_loads AS c
 WHERE c.id_load = $VARIABLE_ID_LOAD$ AND 
       c.id_client = $VARIABLE_ID_CLIENT$ AND 
       c.avg_Throughput_KB_s = $VARIABLE_AVG_THROUGHPUT_KB_S$ AND 
       c.max_Throughput_KB_s = $VARIABLE_MAX_THROUGHPUT_KB_S$;
