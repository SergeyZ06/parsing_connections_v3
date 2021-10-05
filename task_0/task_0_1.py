import time
import datetime
import requests
from bs4 import BeautifulSoup
import sqlite3

from supportive_functions import get_query
from supportive_functions import db_table_exists
from supportive_functions import db_table_create


# Class for fetching information and saving into SQLite DB.
class ParsingConnections:
    def __init__(self, dict_settings):
        self.start_url = dict_settings['target_url_1']
        self.path_sql_query_0_0 = dict_settings['path_sql_query_0_0']
        self.path_sql_query_0_1 = dict_settings['path_sql_query_0_1']
        self.path_dml_query_0_0 = dict_settings['path_dml_query_0_0']
        self.path_dml_query_0_1 = dict_settings['path_dml_query_0_1']
        self.path_ddl_query_0_0 = dict_settings['path_ddl_query_0_0']
        self.path_db = dict_settings['path_db']

        self.soup = None
        self.timestamp = None
        self.list_sessions = None
        self.report = ''

    def get_response(self, start_url, *args, **kwargs):
        # Check: response should be received in 15 attempts.
        # Else: raise error.
        for _ in range(15):
            response = requests.get(start_url, *args, **kwargs)
            if response.status_code == 200:
                self.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                return response
            time.sleep(1)
        self.report += f'\nError - request has returned without response:\n\t{start_url}'
        return None

    def get_soup(self, *args, **kwargs):
        response = self.get_response(self.start_url, *args, **kwargs)
        if response is not None:
            response = response.text
            self.soup = BeautifulSoup(response, 'lxml')
        else:
            self.soup = None

    def data_processing(self):
        if self.soup is not None:
            # Find table with Active clients.
            self.list_sessions = self.soup.find_all(f'tr')[3:]
            self.report += f'\nData have been received successfully:'

            # For each row in table:
            for line in self.list_sessions:
                str_session = str(line)
                list_session = str_session.split('<td>')

                # get information about client:
                dict_client = {'Process_ID': list_session[1].split('</td>')[0],
                               'Source': list_session[2].split('</td>')[0].split(':')[0],
                               'Source_port': list_session[2].split('</td>')[0].split(':')[1],
                               'Destination': list_session[3].split('</td>')[0].split(':')[0],
                               'Destination_port': list_session[3].split('</td>')[0].split(':')[1]}

                # get information about client's connection:
                dict_connection = {'error': ''}
                # Check: information 'Throughput_KB_s' should be specified.
                # Else: make note into field 'error'.
                if len(list_session) >= 4:
                    if list_session[4].find('</td>') == -1:
                        dict_connection['Throughput_KB_s'] = '0'
                        if dict_connection['error'] != '':
                            dict_connection['error'] += f', '
                        dict_connection['error'] += f'Throughput_KB_s: {list_session[4]}'
                    else:
                        # Check: data should suit pattern ' Kb/sec'.
                        if list_session[4].split('</td>')[0].find(' Kb/sec') == -1:
                            dict_connection['Throughput_KB_s'] = '0'
                            if dict_connection['error'] != '':
                                dict_connection['error'] += f', '
                            dict_connection['error'] = f'Throughput_KB_s: {list_session[4].split("</td>")[0]}'
                        else:
                            dict_connection['Throughput_KB_s'] = list_session[4].split('</td>')[0].split(' Kb/sec')[0]
                else:
                    dict_connection['Throughput_KB_s'] = '0'
                    if dict_connection['error'] != '':
                        dict_connection['error'] += f', '
                    dict_connection['error'] += f'Throughput_KB_s: table cell hasn\'t been discovered'

                dict_connection['timestamp'] = self.timestamp

                self.report += f'\n\t{dict_client}\t{dict_connection}'
                self.db_writing(dict_client, dict_connection)

            if self.report.find('Error') == -1:
                self.report += f'\nData were successfully recorded into the SQLite3 DataBase at ' \
                               f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.'
        else:
            self.report += f'\nWarning - data haven\'t been received!'

    def db_writing(self, dict_client, dict_connection):
        str_query = ''
        try:
            # Check: tables "connections" and "clients" should exist.
            # Else: create tables "connections" and "clients".
            db_table_exists_result, db_table_exists_report = db_table_exists(self.path_db, self.path_sql_query_0_0,
                                                                             count_tables=2)
            self.report += db_table_exists_report

            if db_table_exists_result is False:
                self.report += db_table_create(self.path_db, self.path_ddl_query_0_0)

            sqlite_connection = sqlite3.connect(self.path_db)

            # Looking for id_client among already recorded clients.
            str_sql_query_0_1 = get_query(self.path_sql_query_0_1)
            str_sql_query_0_1 = str_sql_query_0_1.replace('$VARIABLE_PROCESS_ID$', dict_client['Process_ID'])
            str_sql_query_0_1 = str_sql_query_0_1.replace('$VARIABLE_SOURCE$', dict_client['Source'])
            str_sql_query_0_1 = str_sql_query_0_1.replace('$VARIABLE_SOURCE_PORT$', dict_client['Source_port'])
            str_sql_query_0_1 = str_sql_query_0_1.replace('$VARIABLE_DESTINATION$', dict_client['Destination'])
            str_sql_query_0_1 = str_sql_query_0_1.replace('$VARIABLE_DESTINATION_PORT$',
                                                          dict_client['Destination_port'])
            str_query = str_sql_query_0_1
            dict_connection['id_client'] = sqlite_connection.execute(str_query).fetchone()
            # Check: if client doesn't exist, make a new client record into the table 'clients'.
            if dict_connection['id_client'] is None:
                str_dml_query_0_0 = get_query(self.path_dml_query_0_0)
                str_dml_query_0_0 = str_dml_query_0_0.replace('$VARIABLE_PROCESS_ID$', dict_client['Process_ID'])
                str_dml_query_0_0 = str_dml_query_0_0.replace('$VARIABLE_SOURCE$', dict_client['Source'])
                str_dml_query_0_0 = str_dml_query_0_0.replace('$VARIABLE_SOURCE_PORT$', dict_client['Source_port'])
                str_dml_query_0_0 = str_dml_query_0_0.replace('$VARIABLE_DESTINATION$', dict_client['Destination'])
                str_dml_query_0_0 = str_dml_query_0_0.replace('$VARIABLE_DESTINATION_PORT$',
                                                              dict_client['Destination_port'])
                str_query = str_dml_query_0_0
                sqlite_connection.execute(str_query)
                # Getting id_client from the SQL response.
                str_query = str_sql_query_0_1
                dict_connection['id_client'] = str(sqlite_connection.execute(str_query).fetchone()[0])
            else:
                # If client already exists, get id_client from the SQL response.
                dict_connection['id_client'] = str(dict_connection['id_client'][0])

            # Recording data about connection.
            str_dml_query_0_1 = get_query(self.path_dml_query_0_1)
            str_dml_query_0_1 = str_dml_query_0_1.replace('$VARIABLE_ID_CLIENT$', dict_connection['id_client'])
            str_dml_query_0_1 = str_dml_query_0_1.replace('$VARIABLE_THROUGHPUT_KB_S$',
                                                          dict_connection['Throughput_KB_s'])
            str_dml_query_0_1 = str_dml_query_0_1.replace('$TIMESTAMP$', dict_connection['timestamp'])
            if dict_connection['error'] == '':
                dict_connection['error'] = 'NULL'
            else:
                dict_connection['error'] = f"'{dict_connection['error']}'"
            str_dml_query_0_1 = str_dml_query_0_1.replace('$ERROR$', dict_connection['error'])

            str_query = str_dml_query_0_1
            sqlite_connection.execute(str_query)
            sqlite_connection.commit()
            sqlite_connection.close()

        except sqlite3.Error as sqlite_error:
            str_error = f'\nError - SQLite3 error: {sqlite_error}' \
                        f'\nDataBase file\'s path:' \
                        f'\n\t{self.path_db}' \
                        f'\nQuery:' \
                        f'\n{str_query}'
            self.report += str_error

    def start(self):
        self.get_soup()
        self.data_processing()
        return self.report
