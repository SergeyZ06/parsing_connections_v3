-- sql_query_3_0
-- This query provides list of the nearest active clients.

SELECT co.id_client,
       co.timestamp,
       co.Throughput_KB_s
  FROM connections AS co
 WHERE CAST ( (julianday('NOW') - julianday(co.timestamp) ) * 24 AS REAL) < 21;
