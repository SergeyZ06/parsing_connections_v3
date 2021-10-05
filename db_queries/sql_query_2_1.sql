-- sql_query_2_1
-- This query provides list of dates 'year-month' that should be
-- processed into the table 'loads'.

WITH t1 AS (-- This CTE provides list of dates 'year-month' from the table 'session'.
    SELECT DISTINCT STRFTIME('%Y-%m', s.timestamp) AS dates
      FROM connections AS s
),
t2 AS (-- This CTE provides list of dates 'year-month' from the table 'duration'.
    SELECT DISTINCT STRFTIME('%Y-%m', s.timestamp_first) AS dates
      FROM loads AS s
)
-- This query provides list of dates 'year-month' that present in
-- the table 'sessions' and absent in the table 'duration'.
-- Current date won't be considered.
SELECT t1.dates
  FROM t1
 WHERE t1.dates NOT IN (
           SELECT t2.dates
             FROM t2
       )
AND 
       t1.dates <> STRFTIME('%Y-%m', DATE('now', 'localtime') );
