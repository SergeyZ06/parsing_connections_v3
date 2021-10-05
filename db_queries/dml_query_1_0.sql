-- dml_query_1_0
-- This query records data into the table 'durations' according to the task:
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
           SUM(t1.timestamp_delta) AS duration_seconds,
           MIN(t1.timestamp) AS timestamp_first,
           MAX(t1.timestamp_next) AS timestamp_last
      FROM t1
     WHERE t1.timestamp_delta BETWEEN 270 AND 330
     GROUP BY t1.id_client
)
INSERT INTO durations (-- This query records data into the table 'duration'.
                          id_client,
                          duration_seconds,
                          timestamp_first,
                          timestamp_last
                      )-- This query calculates a duration of the each session.
                      SELECT t2.id_client,
                             t2.duration_seconds,
                             t2.timestamp_first,
                             t2.timestamp_last
                        FROM t2;
