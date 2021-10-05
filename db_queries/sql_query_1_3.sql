-- sql_query_1_3
-- This query represents data from the table 'durations'.

SELECT ROW_NUMBER() OVER (ORDER BY d.timestamp_last ASC,
       d.timestamp_first ASC,
       d.id_client ASC) AS row_number,
       cl.Process_ID,
       cl.Source,
       cl.Source_port,
       cl.Destination,
       cl.Destination_port,
       d.duration_seconds / (60 * 60 * 24) AS days,
       (d.duration_seconds % (60 * 60 * 24) ) / (60 * 60) AS hours,
       (d.duration_seconds % (60 * 60) ) / 60 AS minutes,
       d.duration_seconds % 60 AS seconds,
       d.timestamp_first,
       d.timestamp_last
  FROM durations AS d
       INNER JOIN
       clients AS cl ON cl.id_client = d.id_client
 WHERE STRFTIME('%Y-%m', d.timestamp_first) = '$VARIABLE_DATE$';
