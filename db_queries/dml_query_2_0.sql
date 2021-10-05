-- dml_query_2_0
-- This query records data into the table 'loads' according to the task:
-- 2) Определить дату (время) когда было максимальное количество активных подключений клиентов и перечень активных клиентов,
-- суммарная нагрузка на канал (Throughput) в этот момент. За месяц и за год.

INSERT INTO loads (
                      count_clients,
                      timestamp_first,
                      timestamp_last,
                      avg_Throughput_KB_s,
                      max_Throughput_KB_s
                  )
                  VALUES (
                      $VARIABLE_COUNT_CLIENTS$,
                      '$VARIABLE_TIMESTAMP_FIRST$',
                      '$VARIABLE_TIMESTAMP_LAST$',
                      $VARIABLE_AVG_THROUGHPUT_KB_S$,
                      $VARIABLE_MAX_THROUGHPUT_KB_S$
                  );
