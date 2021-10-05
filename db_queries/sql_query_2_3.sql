-- sql_query_2_3
-- This query provides information from the table 'loads':

SELECT l.id_load
  FROM loads AS l
 WHERE l.count_clients = $VARIABLE_COUNT_CLIENTS$ AND 
       STRFTIME('%Y-%m-%d %H:%M:%S', l.timestamp_first) = '$VARIABLE_TIMESTAMP_FIRST$' AND 
       STRFTIME('%Y-%m-%d %H:%M:%S', l.timestamp_last) = '$VARIABLE_TIMESTAMP_LAST$' AND 
       l.avg_Throughput_KB_s = $VARIABLE_AVG_THROUGHPUT_KB_S$ AND 
       l.max_Throughput_KB_s = $VARIABLE_MAX_THROUGHPUT_KB_S$;
