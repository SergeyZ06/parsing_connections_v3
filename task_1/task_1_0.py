# 1) Подсчитать общее время просмотра каналов (Destination).
# Таблица: с какого адреса, на какой адрес:порт, общее время просмотра за месяц, за год.

import sqlite3
import time
import datetime

from supportive_functions import get_query
from supportive_functions import db_table_exists
from supportive_functions import db_table_create


# Class for reading a table 'connections', calculating connections' duration
# and recording it into a table 'duration'.
class ConnectionsDuration:
    def __init__(self, dict_settings):
        self.path_sql_query_0_0 = dict_settings['path_sql_query_0_0']
        self.path_sql_query_1_0 = dict_settings['path_sql_query_1_0']
        self.path_sql_query_1_1 = dict_settings['path_sql_query_1_1']
        self.path_ddl_query_1_0 = dict_settings['path_ddl_query_1_0']
        self.path_dml_query_1_0 = dict_settings['path_dml_query_1_0']
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
                # Check: table 'duration' should exist.
                # Else: print warning and create table.
                db_table_exists_result, db_table_exists_report = db_table_exists(self.path_db, self.path_sql_query_1_0,
                                                                                 count_tables=1)
                self.report += db_table_exists_report

                if db_table_exists_result is False:
                    self.report += f'\nWarning - table "duration" of SQLite3 DataBase hasn\'t been located at' \
                                   f' following path:' \
                                   f'\n\t{self.path_db}' \
                                   f'\nTable "duration" will be created now:'
                    self.report += db_table_create(self.path_db, self.path_ddl_query_1_0)
                else:
                    self.report += f'\nTable "duration" of SQLite3 DataBase has been successfully located at' \
                                   f' following path:' \
                                   f'\n\t{self.path_db}.'

                # Fetch list of dates that should be precessed.
                sqlite_connection = sqlite3.connect(self.path_db)
                str_query = get_query(self.path_sql_query_1_1)
                sqlite_list_dates_response = sqlite_connection.execute(str_query).fetchall()
                if sqlite_list_dates_response:
                    for sqlite_date in sqlite_list_dates_response:
                        sqlite_list_dates.append(sqlite_date[0])

                # Check: if list of dates is empty, print message.
                # If not: calculate data and insert into the table 'durations'.
                if len(sqlite_list_dates) == 0:
                    self.report += f'\nTable "connections" has no new records for calculation of duration.'
                else:
                    for sqlite_date in sqlite_list_dates:
                        self.report += f'\nCalculation for date "{sqlite_date}" hasn\'t been discovered in the table' \
                                       f' "duration" and will be prepared now:' \
                                       f'\n\tcalculation started at {datetime.datetime.now()};'
                        str_query = get_query(self.path_dml_query_1_0).replace(r'$VARIABLE_DATE$', sqlite_date)
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
                           f'\nImpossible to execute calculation of connections\' duration.'

        return self.report
