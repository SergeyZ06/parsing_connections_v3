-- sql_query_1_2
-- This query calculates connections' monthly duration according to the task:
-- 1) Подсчитать общее время просмотра каналов (Destination).
-- Таблица: с какого адреса, на какой адрес:порт, общее время просмотра за месяц, за год.

WITH t1 AS (-- This CTE calculates a duration between the nearest records inside one connection.
    SELECT co.id_client,
           co.timestamp,
           LEAD(co.timestamp) OVER (PARTITION BY co.id_client ORDER BY co.id_connection) AS timestamp_next,
           CAST (ROUND(CAST ( (julianday(LEAD(co.timestamp) OVER (PARTITION BY co.id_client ORDER BY co.id_connection) ) - julianday(co.timestamp) ) * 24 * 60 * 60 AS REAL) ) AS INTEGER) AS timestamp_delta
      FROM connections AS co
     WHERE STRFTIME('%Y-%m', co.timestamp) = '$VARIABLE_DATE$'
),
t2 AS (-- This query calculates a duration of the each connection.
    SELECT t1.id_client,
           SUM(t1.timestamp_delta) / (60 * 60 * 24) AS days,
           (SUM(t1.timestamp_delta) % (60 * 60 * 24) ) / (60 * 60) AS hours,
           (SUM(t1.timestamp_delta) % (60 * 60) ) / 60 AS minutes,
           SUM(t1.timestamp_delta) % 60 AS seconds,
           MIN(t1.timestamp) AS timestamp_first,
           MAX(t1.timestamp_next) AS timestamp_last
      FROM t1
     WHERE t1.timestamp_delta BETWEEN 270 AND 330
     GROUP BY t1.id_client
)
SELECT ROW_NUMBER() OVER (ORDER BY t2.timestamp_last ASC,
       t2.timestamp_first ASC,
       t2.id_client ASC) AS row_number,
       cl.Process_ID,
       cl.Source,
       cl.Source_port,
       cl.Destination,
       cl.Destination_port,
       t2.days,
       t2.hours,
       t2.minutes,
       t2.seconds,
       t2.timestamp_first,
       t2.timestamp_last
  FROM t2
       INNER JOIN
       clients AS cl ON cl.id_client = t2.id_client;
