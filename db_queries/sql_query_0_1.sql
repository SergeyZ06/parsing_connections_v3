-- sql_query_0_1
-- This query provides information about existence of 'id_client' in the table 'clients':

SELECT cl.id_client
  FROM clients AS cl
 WHERE cl.Process_ID = $VARIABLE_PROCESS_ID$ AND 
       cl.Source = '$VARIABLE_SOURCE$' AND 
       cl.Source_port = $VARIABLE_SOURCE_PORT$ AND 
       cl.Destination = '$VARIABLE_DESTINATION$' AND 
       cl.Destination_port = $VARIABLE_DESTINATION_PORT$;
