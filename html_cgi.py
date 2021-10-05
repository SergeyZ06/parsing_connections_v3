#!/bin/python3.7

# 1) Подсчитать общее время просмотра каналов (Destination).
# Таблица: с какого адреса, на какой адрес:порт, общее время просмотра за месяц, за год.
#
# 2) Определить дату (время) когда было максимальное количество активных подключений клиентов
# и перечень активных клиентов, суммарная нагрузка на канал (Throughput) в этот момент. За месяц и за год.
#
# 3) Графики:
# - количество активных подключений по шкале времени (как в дюде с масштабом по времени)
# - суммарный Throughput по шкале времени (как в дюде с масштабом по времени)
# - количество подключений по шкале источников видео (Destination) с указанием клиентов (Source)
#
# Что происходит с программой если ресурс не доступен? В данных должно быть поле:
# отсутствие или наличие подключения (доступности) ресурса.
# Соответственно график работает / не работает по шкале времени.
# Таблица с событиями: время когда перестал работать, время когда восстановился и время недоступности.
# Также общее время не работы за месяц и за год.

import time
import datetime
import cgi
import cgitb
# import os
# import sys
# import sqlite3

from task_0.task_0_0 import SettingsReader
from task_1.task_1_0 import ConnectionsDuration
from task_1.task_1_1 import DurationToHTML
from task_2.task_2_0 import ConnectionsLoad
from task_2.task_2_1 import LoadToHTML
from supportive_functions import get_text
from supportive_functions import db_table_create


if __name__ == '__main__':
    script_name = f'parsing_connections'

    # Reading settings.ini
    reader = SettingsReader()
    dict_settings, report_0_0 = reader.read_settings()

    if dict_settings is None:
        report = f'Content-type:text/html\n\n\n<html>\n<body>\n$VARIABLE_REPORT$\n</body>\n</html>'
        message_error = f'The script "{script_name}" has finished with error:' \
                        f'\n{report_0_0}'
        report = report.replace('$VARIABLE_REPORT$', message_error)
        print(report)
        time.sleep(1)
        raise SystemExit()

    if dict_settings['settings_check'] is False:
        report = f'Content-type:text/html\n\n\n<html>\n<body>\n$VARIABLE_REPORT$\n</body>\n</html>'
        message_error = f'The script "{script_name}" has finished with error:' \
                        f'\n{report_0_0}'
        report = report.replace('$VARIABLE_REPORT$', message_error)
        print(report)
        time.sleep(1)
        raise SystemExit()

    cgitb.enable(display=0, logdir='/home/zsv/logs')

    cgi_form = cgi.FieldStorage()
    cgi_data_duration = cgi_form.getvalue('dropdown_date_duration')
    cgi_data_load = cgi_form.getvalue('dropdown_date_load')
    cgi_data_recalculation = cgi_form.getvalue('dropdown_date_recalculation')

    if cgi_data_duration is not None:
        process_task_1_1 = DurationToHTML(dict_settings=dict_settings, date_duration=cgi_data_duration)
        process_task_1_1.print_html()
        # # command = f'.{os.path.abspath(sys.argv[0])} duration {cgi_data_duration} 300'
        # command = f'{sys.argv[0]} duration {cgi_data_duration} 300'
        # os.system(command)
        # exit()
    elif cgi_data_load is not None:
        process_task_2_1 = LoadToHTML(dict_settings=dict_settings, date_load=cgi_data_load)
        process_task_2_1.print_html()
        # # command = f'.{os.path.abspath(sys.argv[0])} load {cgi_data_load} 300'
        # command = f'{sys.argv[0]} load {cgi_data_load} 300'
        # os.system(command)
        # exit()
    elif cgi_data_recalculation is not None:
        report = ''

        dict_settings['path_db'] = dict_settings['path_db'].replace(datetime.datetime.now().strftime("%Y"),
                                                                    cgi_data_recalculation.split('-')[1])

        document_html = get_text(path_file_text=dict_settings['path_html_task_1_0'])
        document_html = document_html.replace('$VARIABLE_DATE$', f'recalculation table "{cgi_data_recalculation}"')
        document_html = document_html.replace('$VARIABLE_REFRESH$', '')
        document_html = document_html.replace('$VARIABLE_TASK$',
                                              f'Recalculation a table "{cgi_data_recalculation}"'
                                              f' has been initiated.')

        if cgi_data_recalculation.split('-')[0] == 'Duration':
            report += db_table_create(path_db=dict_settings['path_db'], path_query=dict_settings['path_ddl_query_1_1'])
            process_task_1_0 = ConnectionsDuration(dict_settings=dict_settings)
            report += process_task_1_0.start()
        elif cgi_data_recalculation.split('-')[0] == 'Load':
            report += db_table_create(path_db=dict_settings['path_db'], path_query=dict_settings['path_ddl_query_2_1'])
            process_task_2_0 = ConnectionsLoad(dict_settings=dict_settings)
            report += process_task_2_0.start()
        else:
            report += '\nTable from CGI data hasn\'t been recognised.'

        document_html = document_html.replace('$VARIABLE_DATA$', report)
        print(document_html)

    # elif len(sys.argv) > 3:
    #     if sys.argv[1] == 'duration':
    #         time.sleep(int(sys.argv[3]))
    #         process_task_1_1 = DurationToHTML(dict_settings=dict_settings, date_duration=sys.argv[2])
    #         process_task_1_1.print_html()
    #         # command = f'.{os.path.abspath(sys.argv[0])} duration {sys.argv[2]} 300'
    #         command = f'{sys.argv[0]} duration {sys.argv[2]} 300'
    #         os.system(command)
    #         exit()
    #     elif sys.argv[1] == 'load':
    #         time.sleep(int(sys.argv[3]))
    #         process_task_2_1 = LoadToHTML(dict_settings=dict_settings, date_load=sys.argv[2])
    #         process_task_2_1.print_html()
    #         # command = f'.{os.path.abspath(sys.argv[0])} load {sys.argv[2]} 300'
    #         command = f'{sys.argv[0]} load {sys.argv[2]} 300'
    #         os.system(command)
    #         exit()
    else:
        document_html = f'Content-type:text/html\n\n\n<html>\n<body>\n$VARIABLE_REPORT$\n</body>\n</html>'
        message_error = f'The script "{script_name}" has finished with error:' \
                        f'\n{report_0_0}' \
                        f'\n\nNo CGI data has been received.'
        document_html = document_html.replace('$VARIABLE_REPORT$', message_error)
        print(document_html)
