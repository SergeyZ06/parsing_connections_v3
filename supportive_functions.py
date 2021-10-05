import sqlite3
import datetime


# Function for getting text of query from query file.
# Return: text of the query.
def get_query(path_query):
    with open(file=path_query, mode='r', encoding='utf-8') as file_query:
        # Variable is to store query string
        query = file_query.read()
        return query


# Function for getting text from file.
# Return: text.
def get_text(path_file_text):
    with open(file=path_file_text, mode='r', encoding='utf-8') as file_query:
        text = file_query.read()
        return text


# Function for checking if table exists.
# Return: True or False.
def db_table_exists(path_db, path_query, count_tables):
    str_query = get_query(path_query)

    try:
        sqlite_connection = sqlite3.connect(path_db)

        # Check: if table exists
        if sqlite_connection.execute(str_query).fetchone()[0] == count_tables:
            sqlite_connection.close()
            return True, ''
        else:
            sqlite_connection.close()
            return False, ''

    except sqlite3.Error as sqlite_error:
        str_error = f'\nError - SQLite3 error: {sqlite_error}' \
                    f'\nDataBase file\'s path:' \
                    f'\n\t{path_db}' \
                    f'\nQuery:' \
                    f'\n{str_query}'
        return False, str_error


# Function for creating a new table.
# Return: error message in case of error.
def db_table_create(path_db, path_query):
    str_query = get_query(path_query)

    try:
        sqlite_connection = sqlite3.connect(path_db)
        sqlite_connection.executescript(str_query)
        sqlite_connection.commit()
        sqlite_connection.close()
        return ''

    except sqlite3.Error as sqlite_error:
        str_error = f'\nError - SQLite3 error: {sqlite_error}' \
                    f'\nDataBase file\'s path:' \
                    f'\n\t{path_db}' \
                    f'\nQuery:' \
                    f'\n{str_query}'
        return str_error


# Function for getting data from a table of SQLite DataBase.
# Return: dictionary with rows of query result.
def get_data_from_table(path_db, text_query, messages_error=True):
    dict_response = {}

    try:
        sqlite_connection = sqlite3.connect(path_db)

        dict_row_number = 1
        sqlite_cursor = sqlite_connection.cursor()

        for row_response in sqlite_cursor.execute(text_query).fetchall():
            if dict_row_number == 1:
                dict_response[0] = tuple(map(lambda x: x[0], sqlite_cursor.description))

            dict_response[dict_row_number] = row_response
            dict_row_number += 1

        sqlite_connection.close()

        return dict_response

    except sqlite3.Error as sqlite_error:
        if messages_error:
            str_error = f'\nError - SQLite3 error: {sqlite_error}' \
                        f'\nDataBase file\'s path:' \
                        f'\n\t{path_db}' \
                        f'\nQuery:' \
                        f'\n{text_query}'
            return str_error


# Function for generating html table with data from received dictionary.
# Return: string with html table.
def generate_html_table_duration(dict_data):
    dict_rows = len(dict_data)
    dict_cols = len(dict_data[0])

    html_table = '<table style="border: 1px solid black" cellspacing="0" cellpadding="5">'
    for i in range(dict_rows):
        if i == 0:
            tag_1 = '<b>'
            tag_2 = '</b>'
            tag_3 = ' bgcolor="#dbfaff"'
        else:
            tag_1 = ''
            tag_2 = ''

            if i % 2 == 0:
                tag_3 = ' bgcolor="#edfdff"'
            else:
                tag_3 = ''

        if str(dict_data[i][len(dict_data[i]) - 1])[:-6] == datetime.datetime.now().strftime('%Y-%m-%d %H')\
                and (int(str(dict_data[i][len(dict_data[i]) - 1])[-5:-3]) >=
                     int(datetime.datetime.now().strftime('%M')) - 5):
            tag_3 = ' bgcolor="#d4ffdb"'

        html_table += f'\n\t\t\t<tr style="border: 1px solid black"{tag_3}>'
        for j in range(dict_cols):
            html_table += f'\n\t\t\t\t<td style="border: 1px solid black">{tag_1}{dict_data[i][j]}{tag_2}</td>'
        html_table += '\n\t\t\t</tr">'
    html_table += '\n\t\t</table>'
    return html_table


# Function for generating html table with data from received dictionary.
# Return: string with html table.
def generate_html_table_load(dict_data):
    dict_rows = len(dict_data)
    dict_cols = len(dict_data[0])
    dict_colors = {
        0: ' bgcolor="#edfdff"',
        1: ' bgcolor="#f7f0ea"',
        2: ' bgcolor="#fffca8"',
        3: ' bgcolor="#ffedbd"',
        4: ' bgcolor="#ffd9a8"',
        5: ' bgcolor="#ffc2a8"',
        6: ' bgcolor="#ffa8bd"',
        7: ' bgcolor="#e4bfff"',
        8: ' bgcolor="#c9bfff"',
        9: ' bgcolor="#bfdeff"'
    }

    html_table = '<table style="border: 1px solid black" cellspacing="0" cellpadding="5">'

    id_color = 0
    timestamp_first_j = 0
    timestamp_last_j = 0

    for i in range(dict_rows):
        if i == 0:
            tag_1 = '<b>'
            tag_2 = '</b>'
            tag_3 = ' bgcolor="#dbfaff"'
        else:
            tag_1 = ''
            tag_2 = ''

            if i > 1:
                if (dict_data[i][timestamp_first_j] != dict_data[i - 1][timestamp_first_j]) \
                        or (dict_data[i][timestamp_last_j] != dict_data[i - 1][timestamp_last_j]):
                    id_color += 1
                    if id_color == 10:
                        id_color = 0
            tag_3 = dict_colors[id_color]

        html_table += f'\n\t\t\t<tr style="border: 1px solid black"{tag_3}>'
        for j in range(dict_cols):
            html_table += f'\n\t\t\t\t<td style="border: 1px solid black">{tag_1}{dict_data[i][j]}{tag_2}</td>'
            if str(dict_data[i][j]) == 'timestamp_first':
                timestamp_first_j = j
            if str(dict_data[i][j]) == 'timestamp_last':
                timestamp_last_j = j
        html_table += '\n\t\t\t</tr">'
    html_table += '\n\t\t</table>'
    return html_table
