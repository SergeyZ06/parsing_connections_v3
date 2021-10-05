-- sql_query_2_7
-- This query calculates connections' yearly load according to the task:
-- 2) Определить дату (время) когда было максимальное количество активных подключений клиентов и перечень активных клиентов,
-- суммарная нагрузка на канал (Throughput) в этот момент. За месяц и за год.

WITH t1 AS (-- This CTE calculates count of clients, sum of throughput and list of clients for each timestamp.
    SELECT co.id_client,
           co.Throughput_KB_s,
           co.timestamp,
           COUNT(co.id_client) OVER (PARTITION BY co.timestamp) AS count_clients,
           ROUND(SUM(co.Throughput_KB_s) OVER (PARTITION BY co.timestamp), 2) AS sum_Throughput_KB_s,
           GROUP_CONCAT(co.id_client) OVER (PARTITION BY co.timestamp) AS list_clients
      FROM connections AS co
     WHERE STRFTIME('%Y-%m', co.timestamp) = '$VARIABLE_DATE$-' || STRFTIME('%m', datetime('now', 'localtime') ) 
),
t2 AS (-- This CTE represents summary about each client.
    SELECT t1.count_clients,
           MIN(t1.timestamp) AS timestamp_first,
           MAX(t1.timestamp) AS timestamp_last,
           ROUND(AVG(sum_Throughput_KB_s), 2) AS avg_Throughput_KB_s,
           MAX(sum_Throughput_KB_s) AS max_Throughput_KB_s,
           t1.id_client,
           ROUND(AVG(Throughput_KB_s), 2) AS avg_client_Throughput_KB_s,
           MAX(Throughput_KB_s) AS max_client_Throughput_KB_s
      FROM t1
     WHERE t1.count_clients = (
                                  SELECT MAX(COUNT(t11.id_client) ) OVER () 
                                    FROM t1 AS t11
                                   GROUP BY t11.timestamp
                              )
     GROUP BY t1.id_client,
              t1.count_clients,
              t1.list_clients
    UNION
    SELECT l.count_clients,
           l.timestamp_first,
           l.timestamp_last,
           l.avg_Throughput_KB_s,
           l.max_Throughput_KB_s,
           c.id_client,
           c.avg_Throughput_KB_s AS avg_client_Throughput_KB_s,
           c.max_Throughput_KB_s AS max_client_Throughput_KB_s
      FROM loads AS l
           INNER JOIN
           clients_in_loads AS c ON c.id_load = l.id_load
     WHERE STRFTIME('%Y', l.timestamp_first) = '$VARIABLE_DATE$'
)
SELECT ROW_NUMBER() OVER (ORDER BY t2.timestamp_last ASC,
       t2.timestamp_first ASC,
       cl.id_client ASC) AS row_number,
       t2.count_clients,
       t2.timestamp_first,
       t2.timestamp_last,
       t2.avg_Throughput_KB_s,
       t2.max_Throughput_KB_s,
       cl.Process_ID,
       cl.Source,
       cl.Source_port,
       cl.Destination,
       cl.Destination_port,
       t2.avg_client_Throughput_KB_s,
       t2.max_client_Throughput_KB_s
  FROM t2
       INNER JOIN
       clients AS cl ON cl.id_client = t2.id_client
 WHERE t2.count_clients = (
                              SELECT MAX(t3.count_clients) 
                                FROM t2 AS t3
                          );
