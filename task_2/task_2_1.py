# 2) Определить дату (время) когда было максимальное количество активных подключений клиентов
# и перечень активных клиентов, суммарная нагрузка на канал (Throughput) в этот момент. За месяц и за год.

import datetime

from supportive_functions import get_text
from supportive_functions import get_query
from supportive_functions import get_data_from_table
from supportive_functions import generate_html_table_load


# Class for representation monthly connections' loads as html document for Apache2.
class LoadToHTML:
    def __init__(self, dict_settings, date_load):
        self.path_sql_query_2_5 = dict_settings['path_sql_query_2_5']
        self.path_sql_query_2_6 = dict_settings['path_sql_query_2_6']
        self.path_sql_query_2_7 = dict_settings['path_sql_query_2_7']
        self.path_sql_query_2_8 = dict_settings['path_sql_query_2_8']
        self.path_db = dict_settings['path_db']
        self.path_html_task_1_0 = dict_settings['path_html_task_1_0']
        self.sqlite_date = date_load
        self.path_description_task_2 = dict_settings['description_task_2']

    def create_html(self):
        # Loading html pattern.
        document_html = get_text(self.path_html_task_1_0)
        str_task = get_text(self.path_description_task_2)
        document_html = document_html.replace('$VARIABLE_TASK$', str_task)

        # If date isn't received:
        if type(self.sqlite_date) != str:
            dict_data = None
            document_html = document_html.replace(r'$VARIABLE_DATE$', 'None')
        else:
            document_html = document_html.replace(r'$VARIABLE_DATE$', self.sqlite_date)

            if self.sqlite_date == datetime.datetime.now().strftime("%Y-%m"):
                document_html = document_html.replace('$VARIABLE_REFRESH$', '<meta http-equiv="refresh" content="60">')
            elif self.sqlite_date == datetime.datetime.now().strftime("%Y"):
                document_html = document_html.replace('$VARIABLE_REFRESH$', '<meta http-equiv="refresh" content="60">')
            else:
                document_html = document_html.replace('$VARIABLE_REFRESH$', '')

            self.path_db = self.path_db.replace(datetime.datetime.now().strftime("%Y"), self.sqlite_date.split('-')[0])

            if self.sqlite_date.find('-') != -1:
                # Date format YYYY-MM.
                # Check: if solicited date equals current date:
                if self.sqlite_date == datetime.datetime.now().strftime("%Y-%m"):
                    # calculate data from the table 'connections'.
                    str_query = get_query(self.path_sql_query_2_5).replace('$VARIABLE_DATE$', self.sqlite_date)
                else:
                    # get data from tables "loads" and "clients_in_loads".
                    str_query = get_query(self.path_sql_query_2_6).replace('$VARIABLE_DATE$', self.sqlite_date)
            else:
                # Date format YYYY.
                # Check: if solicited date equals current date:
                if self.sqlite_date == datetime.datetime.now().strftime("%Y"):
                    # calculate data from the table 'connections'.
                    str_query = get_query(self.path_sql_query_2_7).replace('$VARIABLE_DATE$', self.sqlite_date)
                else:
                    # get data from tables "loads" and "clients_in_loads".
                    str_query = get_query(self.path_sql_query_2_8).replace('$VARIABLE_DATE$', self.sqlite_date)

            dict_data = get_data_from_table(self.path_db, str_query)

        # If requested data is absent:
        if (dict_data is None) or (dict_data == {}):
            # prepare a message.
            document_html_content = "<p>There aren't any records according to the specified date.</p>"
        elif type(dict_data) == str:
            # If SQL error has occurred:
            if dict_data.find('no such table') != -1:
                # print a message in case of absence of data.
                document_html_content = "<p>There aren't any records according to the specified date.</p>"
            else:
                # print SQL report otherwise.
                document_html_content = f'<p>{dict_data}</p>'
        else:
            # prepare a table with requested data.
            document_html_content = generate_html_table_load(dict_data)

        document_html = document_html.replace('$VARIABLE_DATA$', document_html_content)

        return document_html

    def print_html(self):
        document_html = self.create_html()
        print(f'{document_html}')
