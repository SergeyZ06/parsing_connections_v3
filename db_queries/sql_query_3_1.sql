-- sql_query_3_1
-- This query provides info about the nearest active clients.

SELECT cl.Process_ID,
       cl.Source,
       cl.Source_port,
       cl.Destination,
       cl.Destination_port
  FROM clients AS cl
 WHERE cl.id_client = $VARIABLE_ID_CLIENT$;
