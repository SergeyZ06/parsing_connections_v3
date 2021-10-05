-- sql_query_2_0
-- This query provides information about existence of tables 'loads' and 'clients_in_loads':
-- 0 - tables don't exist;
-- 1 - only one table exists;
-- 2 - both tables exist.

SELECT COUNT(sqlite_master.name) AS tables_exists
  FROM sqlite_master
 WHERE sqlite_master.name = 'loads' OR 
       sqlite_master.name = 'clients_in_loads';
