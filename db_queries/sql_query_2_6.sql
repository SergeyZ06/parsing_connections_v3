-- sql_query_2_6
-- This query calculates connections' monthly load according to the task:
-- 2) Определить дату (время) когда было максимальное количество активных подключений клиентов и перечень активных клиентов,
-- суммарная нагрузка на канал (Throughput) в этот момент. За месяц и за год.

SELECT ROW_NUMBER() OVER (ORDER BY l.timestamp_last ASC,
       l.timestamp_first ASC,
       cl.id_client ASC) AS row_number,
       l.count_clients,
       l.timestamp_first,
       l.timestamp_last,
       l.avg_Throughput_KB_s,
       l.max_Throughput_KB_s,
       cl.Process_ID,
       cl.Source,
       cl.Source_port,
       cl.Destination,
       cl.Destination_port,
       c.avg_Throughput_KB_s AS avg_client_Throughput_KB_s,
       c.max_Throughput_KB_s AS max_client_Throughput_KB_s
  FROM loads AS l
       INNER JOIN
       clients_in_loads AS c ON c.id_load = l.id_load
       INNER JOIN
       clients AS cl ON cl.id_client = c.id_client
 WHERE STRFTIME('%Y-%m', l.timestamp_first) = '$VARIABLE_DATE$';
