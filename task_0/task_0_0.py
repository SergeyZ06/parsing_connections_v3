import os
import sys
import platform
import datetime


# Class for reading settings file and checking parameters.
class SettingsReader:
    def __init__(self, file_settings=r'settings.ini', reason='Manually'):
        self.file_settings = file_settings
        self.file_settings_full_path = os.path.join(os.path.dirname(sys.argv[0]), self.file_settings)

        self.dict_settings = {}
        self.report = ''
        self.reason = reason

    # Method for reading parameters from settings file and recording it into the dictionary:
    def read_settings(self):
        self.report += f'\nScript started at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ({self.reason}).'

        # Check: settings file should exist.
        try:
            with open(file=self.file_settings_full_path, mode='r') as file:
                for line in file:
                    if (line.find('=') != -1) and (line[0] != '#'):
                        if line.find('#') != -1:
                            line = line.split('#')[0]
                        key, db_path = line.split('=')
                        key = key.replace('\t', '').replace(' ', '')
                        db_path = db_path.replace('\n', '').replace('\t', '').replace(' ', '')
                        self.dict_settings[key] = db_path
        # If settings file doesn't exist: print an error.
        except FileNotFoundError:
            self.report += f'\nError - configuration file "{self.file_settings}" hasn\'t been located at following' \
                           f' path: ' \
                           f'\n\t{self.file_settings_full_path}' \
                           f'\nMake sure "{self.file_settings}" is located there, otherwise this script won\'t be ' \
                           f'able to launch!'
            return None, self.report

        self.report += f'\nConfiguration file "{self.file_settings}" has been successfully located.'

        # Revise parameters and return it.
        self.check_settings()

        if self.report.find('Error') != -1:
            self.report += f'\nConfiguration file "{self.file_settings}" contains mistakes and cannot be read!'
            self.dict_settings['settings_check'] = False
        else:
            self.report += f'\nConfiguration file "{self.file_settings}" has been successfully read.'
            self.dict_settings['settings_check'] = True

        return self.dict_settings, self.report

    # Method for checking parameters:
    def check_settings(self):
        # Variable is to store operating system name.
        current_platform = platform.system()
        # Variable is to store script directory.
        dir_location = os.path.dirname(sys.argv[0])

        # Function for changing path for operating system.
        def func_path_creation(func_path, func_current_platform, func_dir_location):
            if func_current_platform == 'Windows':
                func_path = func_path.replace('/', '\\')
            else:
                func_path = func_path.replace('\\', '/')
            func_path = os.path.join(func_dir_location, func_path)
            return func_path

        # Variable is to store SQLite BD path.
        path_db = None
        # List is to store all SQLite DB paths.
        list_to_delete = []

        # Searching paths:
        for key in self.dict_settings.keys():
            # Check: all SQL queries should exist.
            # Check: all DDL queries should exist.
            # Check: all DML queries should exist.
            # Check: all html documents should exist.
            if (key.find(r'path_sql_query_') != -1)\
                    or (key.find(r'path_ddl_query_') != -1)\
                    or (key.find(r'path_dml_query_') != -1)\
                    or (key.find(r'path_html_') != -1)\
                    or (key.find(r'description_') != -1):
                # Changing path for operating system.
                self.dict_settings[key] = func_path_creation(func_path=self.dict_settings[key],
                                                             func_current_platform=current_platform,
                                                             func_dir_location=dir_location)
                # If SQL query doesn't exist: print an error.
                if os.path.exists(self.dict_settings[key]) is False:
                    self.report += f'\nError - {key} hasn\'t been located:\n\t{self.dict_settings[key]}'

            # Check: SQLite DB might exist
            if key.find('path_db_') != -1:
                list_to_delete.append(key)
                # Changing path for operating system.
                self.dict_settings[key] = func_path_creation(func_path=self.dict_settings[key],
                                                             func_current_platform=current_platform,
                                                             func_dir_location=dir_location)
                # Appending year timestamp to the DataBase file's name.
                self.dict_settings[key] = self.dict_settings[key].replace('.', datetime.datetime.now().strftime("_%Y."))
                # If SQLite DB exists: use it's path.
                if (os.path.exists(self.dict_settings[key]) is True) and (path_db is None):
                    path_db = self.dict_settings[key]

        # If SQLite DB doesn't exist:
        if path_db is None:
            # If at least one path has been discovered: use it.
            if len(list_to_delete) > 0:
                path_db = self.dict_settings[list_to_delete[0]]
                self.report += f'\nWarning - having read configuration file "{self.file_settings}", ' \
                               f'DataBase file wasn\'t located.' \
                               f'\nNew SQLite3 DataBase will be created at following path:\n\t{path_db}'
            # If no path has been discovered: print an error.
            else:
                self.report += f'\nError - having read configuration file "{self.file_settings}", ' \
                               f'DataBase path wasn\'t discovered.' \
                               f'\nMake sure file "{self.file_settings}" contains at least one parameter "path_db_"!'
        else:
            self.report += f'\nDataBase file "{os.path.basename(path_db)}" has been successfully located at following' \
                           f' path:' \
                           f'\n\t{os.path.abspath(path_db)}'

        # Recording chosen path and removing others.
        self.dict_settings['path_db'] = path_db
        for key in list_to_delete:
            self.dict_settings.pop(key)
