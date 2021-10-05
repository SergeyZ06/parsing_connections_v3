-- sql_query_1_0
-- This query provides information about existence of table 'durations':
-- 0 - table doesn't exist;
-- 1 - table exists.

SELECT COUNT(sqlite_master.name) AS table_exists
  FROM sqlite_master
 WHERE sqlite_master.name = 'durations';
