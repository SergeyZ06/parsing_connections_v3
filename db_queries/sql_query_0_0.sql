-- sql_query_0_0
-- This query provides information about existence of tables 'clients' and 'connections':
-- 0 - tables don't exist;
-- 1 - only one table exists;
-- 2 - both tables exist.

SELECT COUNT(sqlite_master.name) AS tables_exists
  FROM sqlite_master
 WHERE sqlite_master.name = 'clients' OR 
       sqlite_master.name = 'connections';
