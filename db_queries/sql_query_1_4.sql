-- sql_query_1_4
-- This query calculates connections' yearly duration according to the task:
-- 1) Подсчитать общее время просмотра каналов (Destination).
-- Таблица: с какого адреса, на какой адрес:порт, общее время просмотра за месяц, за год.

WITH t1 AS (-- This CTE calculates a duration between the nearest records inside one connection.
    SELECT co.id_client,
           co.timestamp AS timestamp_first,
           LEAD(co.timestamp) OVER (PARTITION BY co.id_client ORDER BY co.id_connection) AS timestamp_last,
           CAST (ROUND(CAST ( (julianday(LEAD(co.timestamp) OVER (PARTITION BY co.id_client ORDER BY co.id_connection) ) - julianday(co.timestamp) ) * 24 * 60 * 60 AS REAL) ) AS INTEGER) AS timestamp_sum
      FROM connections AS co
     WHERE STRFTIME('%Y-%m', co.timestamp) = '$VARIABLE_DATE$-' || STRFTIME('%m', datetime('now', 'localtime') ) 
),
t2 AS (
    SELECT d.id_client,
           d.timestamp_first,
           d.timestamp_last,
           d.duration_seconds
      FROM durations AS d
     WHERE STRFTIME('%Y', d.timestamp_first) = '$VARIABLE_DATE$' AND 
           STRFTIME('%Y', d.timestamp_last) = '$VARIABLE_DATE$'
),
t3 AS (
    SELECT t1.id_client,
           t1.timestamp_first,
           t1.timestamp_last,
           t1.timestamp_sum
      FROM t1
    UNION
    SELECT t2.id_client,
           t2.timestamp_first,
           t2.timestamp_last,
           t2.duration_seconds
      FROM t2
),
t4 AS (-- This query calculates a duration of the each connection.
    SELECT t3.id_client,
           SUM(t3.timestamp_sum) / (60 * 60 * 24) AS days,
           (SUM(t3.timestamp_sum) % (60 * 60 * 24) ) / (60 * 60) AS hours,
           (SUM(t3.timestamp_sum) % (60 * 60) ) / 60 AS minutes,
           SUM(t3.timestamp_sum) % 60 AS seconds,
           MIN(t3.timestamp_first) AS timestamp_first,
           MAX(t3.timestamp_last) AS timestamp_last
      FROM t3
     WHERE t3.timestamp_sum > 270
     GROUP BY t3.id_client
)
SELECT ROW_NUMBER() OVER (ORDER BY t4.timestamp_last ASC,
       t4.timestamp_first ASC,
       t4.id_client ASC) AS row_number,
       cl.Process_ID,
       cl.Source,
       cl.Source_port,
       cl.Destination,
       cl.Destination_port,
       t4.days,
       t4.hours,
       t4.minutes,
       t4.seconds,
       t4.timestamp_first,
       t4.timestamp_last
  FROM t4
       INNER JOIN
       clients AS cl ON cl.id_client = t4.id_client;
