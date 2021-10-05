-- sql_query_1_4
-- This query calculates connections' yearly duration according to the task:
-- 1) Подсчитать общее время просмотра каналов (Destination).
-- Таблица: с какого адреса, на какой адрес:порт, общее время просмотра за месяц, за год.

WITH t1 AS (-- This CTE calculates total duration from the table 'durations'.
    SELECT d.id_client,
           MIN(d.timestamp_first) AS timestamp_first,
           MAX(d.timestamp_last) AS timestamp_last,
           SUM(d.duration_seconds) AS timestamp_sum
      FROM durations AS d
     WHERE STRFTIME('%Y', d.timestamp_first) = '$VARIABLE_DATE$' AND 
           STRFTIME('%Y', d.timestamp_last) = '$VARIABLE_DATE$'
     GROUP BY d.id_client
)-- This query calculates a duration of the each session.
SELECT ROW_NUMBER() OVER (ORDER BY t1.timestamp_last ASC,
       t1.timestamp_first ASC,
       t1.id_client ASC) AS row_number,
       cl.Process_ID,
       cl.Source,
       cl.Source_port,
       cl.Destination,
       cl.Destination_port,
       timestamp_sum / (60 * 60 * 24) AS days,
       (timestamp_sum % (60 * 60 * 24) ) / (60 * 60) AS hours,
       (timestamp_sum % (60 * 60) ) / 60 AS minutes,
       timestamp_sum % 60 AS seconds,
       t1.timestamp_first,
       t1.timestamp_last
  FROM t1
       INNER JOIN
       clients AS cl ON cl.id_client = t1.id_client
 WHERE t1.timestamp_sum > 270;
