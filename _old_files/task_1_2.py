#!/bin/python3.7
# 1) Подсчитать общее время просмотра каналов (Destination).
# Таблица: с какого адреса, на какой адрес:порт, общее время просмотра за месяц, за год.

import cgi
import datetime

from supportive_functions import get_query
from supportive_functions import get_data_from_table
from supportive_functions import generate_html_table_duration


# Class for representation yearly connections' duration as html document for Apache2.
class DurationToHTML12:
    def __init__(self, dict_settings):
        self.path_sql_query_1_4 = dict_settings['path_sql_query_1_4']
        self.path_sql_query_1_5 = dict_settings['path_sql_query_1_5']
        self.path_db = dict_settings['path_db']
        self.path_html_task_1_0 = dict_settings['path_html_task_1_0']
        self.sqlite_date = cgi.FieldStorage().getvalue('dropdown_duration_year')

    def create_html(self):
        # Loading html pattern.
        document_html = get_query(self.path_html_task_1_0)
        str_task = '<p><b>1) Подсчитать общее время просмотра каналов (Destination).</b></p>' \
                   '\n<p>Таблица: с какого адреса, на какой адрес:порт, общее время просмотра за месяц, за год.</p>'
        document_html = document_html.replace('$VARIABLE_TASK$', str_task)

        # If date isn't received:
        if self.sqlite_date is None:
            dict_data = None
            document_html = document_html.replace(r'$VARIABLE_DATE$', 'None')
        else:
            document_html = document_html.replace(r'$VARIABLE_DATE$', self.sqlite_date)
            self.path_db = self.path_db.replace(datetime.datetime.now().strftime("%Y"), self.sqlite_date)

            # Check: if solicited date equals current date:
            if self.sqlite_date == datetime.datetime.now().strftime("%Y"):
                # calculate data from the table 'connections'.
                str_query = get_query(self.path_sql_query_1_4).replace('$VARIABLE_DATE$', self.sqlite_date)
            else:
                # get data from the table 'duration'.
                str_query = get_query(self.path_sql_query_1_5).replace('$VARIABLE_DATE$', self.sqlite_date)

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
            document_html_content = generate_html_table_duration(dict_data)

        document_html = document_html.replace('$VARIABLE_DATA$', document_html_content)

        return document_html

    def print_html(self):
        document_html = self.create_html()
        print(document_html)
