# 2) Определить дату (время) когда было максимальное количество активных подключений клиентов
# и перечень активных клиентов, суммарная нагрузка на канал (Throughput) в этот момент. За месяц и за год.

import sqlite3
import time
import datetime

from supportive_functions import get_query
from supportive_functions import db_table_exists
from supportive_functions import db_table_create


# Class for reading a table 'connections', calculating loads and recording it into a table 'loads'.
class ConnectionsLoad:
    def __init__(self, dict_settings):
        self.path_sql_query_0_0 = dict_settings['path_sql_query_0_0']
        self.path_sql_query_2_0 = dict_settings['path_sql_query_2_0']
        self.path_sql_query_2_1 = dict_settings['path_sql_query_2_1']
        self.path_sql_query_2_2 = dict_settings['path_sql_query_2_2']
        self.path_sql_query_2_3 = dict_settings['path_sql_query_2_3']
        self.path_sql_query_2_4 = dict_settings['path_sql_query_2_4']
        self.path_ddl_query_2_0 = dict_settings['path_ddl_query_2_0']
        self.path_dml_query_2_0 = dict_settings['path_dml_query_2_0']
        self.path_dml_query_2_1 = dict_settings['path_dml_query_2_1']
        self.path_db = dict_settings['path_db']

        self.report = ''

    def start(self):
        # Check: tables "connections" and "clients" should exist.
        db_table_exists_result, db_table_exists_report = db_table_exists(self.path_db, self.path_sql_query_0_0, 2)
        self.report += db_table_exists_report

        if db_table_exists_result is True:
            str_query = ''
            sqlite_list_dates = []
            try:
                # Check: tables "loads" and "clients_in_loads" should exist.
                # Else: print warning and create table.
                db_table_exists_result, db_table_exists_report = db_table_exists(self.path_db, self.path_sql_query_2_0,
                                                                                 count_tables=2)
                self.report += db_table_exists_report

                if db_table_exists_result is False:
                    self.report += f'\nWarning - tables "loads" and "clients_in_loads" of SQLite3 DataBase haven\'t' \
                                   f' been located at following path:' \
                                   f'\n\t{self.path_db}' \
                                   f'\nTables "loads" and "clients_in_loads" will be created now:'
                    self.report += db_table_create(self.path_db, self.path_ddl_query_2_0)
                else:
                    self.report += f'\nTables "loads" and "clients_in_loads" of SQLite3 DataBase have been' \
                                   f' successfully located at following path:' \
                                   f'\n\t{self.path_db}.'

                # Fetch list of dates that should be precessed.
                sqlite_connection = sqlite3.connect(self.path_db)
                str_query = get_query(self.path_sql_query_2_1)
                sqlite_list_dates_response = sqlite_connection.execute(str_query).fetchall()
                if sqlite_list_dates_response:
                    for sqlite_date in sqlite_list_dates_response:
                        sqlite_list_dates.append(sqlite_date[0])

                # Check: if list of dates is empty, print message.
                # If not: calculate data and insert into tables "loads" and "clients_in_loads".
                if len(sqlite_list_dates) == 0:
                    self.report += f'\nTable "connections" has no new records for calculation of load.'
                else:
                    # For each date that is absent in tables "loads" and "clients_in_loads":
                    for sqlite_date in sqlite_list_dates:
                        self.report += f'\nCalculation for date "{sqlite_date}" hasn\'t been discovered in tables' \
                                       f' "loads" and "clients_in_loads" and will be prepared now:' \
                                       f'\n\tcalculation started at {datetime.datetime.now()};'

                        # calculate data about for each client in current load.
                        str_query = get_query(self.path_sql_query_2_2).replace(r'$VARIABLE_DATE$', sqlite_date)
                        sqlite_list_clients = sqlite_connection.execute(str_query).fetchall()

                        # If data has been received:
                        if sqlite_list_clients:
                            # get data about load.
                            dict_load = {'count_client': str(sqlite_list_clients[0][0]),
                                         'timestamp_first': str(sqlite_list_clients[0][1]),
                                         'timestamp_last': str(sqlite_list_clients[0][2]),
                                         'avg_Throughput_KB_s': str(sqlite_list_clients[0][3]),
                                         'max_Throughput_KB_s': str(sqlite_list_clients[0][4])}

                            # Check: load should present in the table 'loads'.
                            str_sql_query_2_3 = get_query(self.path_sql_query_2_3)
                            str_sql_query_2_3 = str_sql_query_2_3.replace('$VARIABLE_COUNT_CLIENTS$',
                                                                          dict_load['count_client'])
                            str_sql_query_2_3 = str_sql_query_2_3.replace('$VARIABLE_TIMESTAMP_FIRST$',
                                                                          dict_load['timestamp_first'])
                            str_sql_query_2_3 = str_sql_query_2_3.replace('$VARIABLE_TIMESTAMP_LAST$',
                                                                          dict_load['timestamp_last'])
                            str_sql_query_2_3 = str_sql_query_2_3.replace('$VARIABLE_AVG_THROUGHPUT_KB_S$',
                                                                          dict_load['avg_Throughput_KB_s'])
                            str_sql_query_2_3 = str_sql_query_2_3.replace('$VARIABLE_MAX_THROUGHPUT_KB_S$',
                                                                          dict_load['max_Throughput_KB_s'])
                            str_query = str_sql_query_2_3
                            id_load = sqlite_connection.execute(str_query).fetchone()

                            # If not: insert new load into the table 'loads' and get id_load.
                            if id_load is None:
                                str_dml_query_2_0 = get_query(self.path_dml_query_2_0)
                                str_dml_query_2_0 = str_dml_query_2_0.replace('$VARIABLE_COUNT_CLIENTS$',
                                                                              dict_load['count_client'])
                                str_dml_query_2_0 = str_dml_query_2_0.replace('$VARIABLE_TIMESTAMP_FIRST$',
                                                                              dict_load['timestamp_first'])
                                str_dml_query_2_0 = str_dml_query_2_0.replace('$VARIABLE_TIMESTAMP_LAST$',
                                                                              dict_load['timestamp_last'])
                                str_dml_query_2_0 = str_dml_query_2_0.replace('$VARIABLE_AVG_THROUGHPUT_KB_S$',
                                                                              dict_load['avg_Throughput_KB_s'])
                                str_dml_query_2_0 = str_dml_query_2_0.replace('$VARIABLE_MAX_THROUGHPUT_KB_S$',
                                                                              dict_load['max_Throughput_KB_s'])
                                str_query = str_dml_query_2_0
                                sqlite_connection.execute(str_query)

                                str_query = str_sql_query_2_3
                                id_load = sqlite_connection.execute(str_query).fetchone()[0]

                            # For each discovered client:
                            for row_client in sqlite_list_clients:
                                # get data about client.
                                dict_client = {'id_load': str(id_load),
                                               'id_client': str(row_client[5]),
                                               'avg_client_Throughput_KB_s': str(row_client[6]),
                                               'max_client_Throughput_KB_s': str(row_client[7])}

                                # Check: client should present in the table 'clients_in_loads'.
                                str_sql_query_2_4 = get_query(self.path_sql_query_2_4)
                                str_sql_query_2_4 = str_sql_query_2_4.replace('$VARIABLE_ID_LOAD$',
                                                                              dict_client['id_load'])
                                str_sql_query_2_4 = str_sql_query_2_4.replace('$VARIABLE_ID_CLIENT$',
                                                                              dict_client['id_client'])
                                str_sql_query_2_4 = str_sql_query_2_4.replace('$VARIABLE_AVG_THROUGHPUT_KB_S$',
                                                                              dict_client['avg_client_Throughput_KB_s'])
                                str_sql_query_2_4 = str_sql_query_2_4.replace('$VARIABLE_MAX_THROUGHPUT_KB_S$',
                                                                              dict_client['max_client_Throughput_KB_s'])

                                str_query = str_sql_query_2_4
                                id_client_in_load = sqlite_connection.execute(str_query).fetchone()

                                # If not: insert new client into the table 'clients_in_loads'.
                                if id_client_in_load is None:
                                    str_dml_query_2_1 = get_query(self.path_dml_query_2_1)
                                    str_dml_query_2_1 = str_dml_query_2_1.replace('$VARIABLE_ID_LOAD$',
                                                                                  dict_client['id_load'])
                                    str_dml_query_2_1 = str_dml_query_2_1.replace('$VARIABLE_ID_CLIENT$',
                                                                                  dict_client['id_client'])
                                    str_dml_query_2_1 = str_dml_query_2_1.replace('$VARIABLE_AVG_THROUGHPUT_KB_S$',
                                                                                  dict_client[
                                                                                      'avg_client_Throughput_KB_s'])
                                    str_dml_query_2_1 = str_dml_query_2_1.replace('$VARIABLE_MAX_THROUGHPUT_KB_S$',
                                                                                  dict_client[
                                                                                      'max_client_Throughput_KB_s'])

                                    str_query = str_dml_query_2_1
                                    sqlite_connection.execute(str_query)

                        self.report += f'\n\tcalculation finished at {datetime.datetime.now()}.'
                        time.sleep(2)

                    sqlite_connection.commit()

                sqlite_connection.close()

            except sqlite3.Error as sqlite_error:
                str_error = f'\nError - SQLite3 error: {sqlite_error}' \
                            f'\nDataBase file\'s path:' \
                            f'\n\t{self.path_db}' \
                            f'\nQuery:' \
                            f'\n{str_query}'
                self.report += str_error

        # If tables "connections" and "clients" don't exist: print warning.
        else:
            self.report += f'\nWarning - tables "connections" and "clients" of SQLite3 DataBase hasn\'t been located' \
                           f' at following path:' \
                           f'\n\t{self.path_db}' \
                           f'\nImpossible to execute calculation of connections\' load.'

        return self.report
