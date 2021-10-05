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
import sys

from task_0.task_0_0 import SettingsReader
from task_0.task_0_1 import ParsingConnections
from task_1.task_1_0 import ConnectionsDuration
from task_2.task_2_0 import ConnectionsLoad


if __name__ == '__main__':
    script_name = f'parsing_connections'

    # Reading settings.ini
    reader = SettingsReader()
    dict_settings, report_0_0 = reader.read_settings()

    if dict_settings is None:
        time.sleep(1)
        raise SystemExit(f'The script "{script_name}" has finished with error:'
                         f'\n{report_0_0}')

    if dict_settings['settings_check'] is False:
        time.sleep(1)
        raise SystemExit(f'The script "{script_name}" has finished with error:'
                         f'\n{report_0_0}')

    if len(sys.argv) > 1:
        if sys.argv[1] == dict_settings['cron_argv']:
            report = ''
            if dict_settings['messages_0_0'] == 'True':
                report += report_0_0.replace('Manually', 'Initiated by Cron')

            # task_0
            # Scraping, parsing and recording data into SQLite3 DataBase
            process_task_0_1 = ParsingConnections(dict_settings=dict_settings)
            report_0_1 = process_task_0_1.start()
            if dict_settings['messages_0_1'] == 'True':
                report += report_0_1

            # task_1
            # Every 2th hour of 1th day of every month:
            # calculate connections' duration
            if datetime.datetime.now().strftime("%d-%H") == dict_settings['schedule_task_1_day_hour']:
                time.sleep(int(dict_settings['schedule_delay']))
                process_task_1_0 = ConnectionsDuration(dict_settings=dict_settings)
                report_1_0 = process_task_1_0.start()
                if dict_settings['messages_1_0'] == 'True':
                    report += report_1_0

            # task_2
            # Every 3th hour of 1th day of every month:
            # calculate connections' load
            if datetime.datetime.now().strftime("%d-%H") == dict_settings['schedule_task_2_day_hour']:
                time.sleep(int(dict_settings['schedule_delay']))
                process_task_2_0 = ConnectionsLoad(dict_settings=dict_settings)
                report_2_0 = process_task_2_0.start()
                if dict_settings['messages_2_0'] == 'True':
                    report += report_2_0

            if report != '':
                print(report[1:])
