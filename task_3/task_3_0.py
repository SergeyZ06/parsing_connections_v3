# 3) Графики:
# - количество активных подключений по шкале времени (как в дюде с масштабом по времени)
# - суммарный Throughput по шкале времени (как в дюде с масштабом по времени)
# - количество подключений по шкале источников видео (Destination) с указанием клиентов (Source)

import os
import sys
import pandas as pd
import plotly
import plotly.graph_objs as go

from supportive_functions import get_query
from supportive_functions import get_data_from_table


class Graph:
    def __init__(self, dict_settings):
        self.path_db = dict_settings['path_db']
        self.path_sql_query_3_0 = dict_settings['path_sql_query_3_0']
        self.path_sql_query_3_1 = dict_settings['path_sql_query_3_1']
        self.path_html_task_3_0 = os.path.join(os.path.dirname(sys.argv[0]), dict_settings['path_html_task_3_0'])

    def run(self):
        # Get list of the nearest active clients.
        str_query = get_query(self.path_sql_query_3_0)
        dict_connections = get_data_from_table(self.path_db, str_query, messages_error=True)

        # Prepare DataFrame of the nearest active clients.
        df_connections = pd.DataFrame(dict_connections)
        df_connections = df_connections.transpose()
        df_connections.columns = df_connections.iloc[0]
        df_connections = df_connections[1:]

        list_id_client = list(df_connections['id_client'].unique())

        # Creating a graph.
        fig = go.Figure(layout=go.Layout(
            # xaxis=dict(title='timestamp'),
            yaxis=dict(title='Throughput_KB_s'),
            legend=dict(xanchor='center',
                        yanchor='bottom')
        ))

        fig.update_layout(title_text='Graphs - Active clients',
                          # legend_title_text='Processes:',
                          legend=dict(
                              x=0.5,
                              y=-1.6
                          ))
        # fig.update_layout(showlegend=False)

        # For each client:
        for id_client in list_id_client:
            # draw individual curve.
            str_query = get_query(self.path_sql_query_3_1)
            str_query = str_query.replace('$VARIABLE_ID_CLIENT$', str(id_client))
            dict_client = get_data_from_table(self.path_db, str_query, messages_error=True)

            df_connection = df_connections[df_connections['id_client'] == id_client]

            process_name = ''
            for i in range(len(dict_client[0])):
                process_name += f'{dict_client[0][i]}: {str(dict_client[1][i])}, '
            process_name = process_name[:-2]

            fig.add_trace(
                go.Scatter(
                    x=df_connection['timestamp'],
                    y=df_connection['Throughput_KB_s'],
                    name=process_name
                )
            )

        # Add total load in the end.
        df_total = df_connections[['timestamp', 'Throughput_KB_s']].copy()
        df_total = df_total.groupby(by=['timestamp']).sum()

        fig.add_trace(
            go.Scatter(
                x=df_total.index,
                y=df_total['Throughput_KB_s'],
                name='Total Throughput_KB_s'
            )
        )

        # Zero line.
        fig.add_hline(y=0)
        # Save graph as HTML document.
        plotly.offline.plot(fig, filename=self.path_html_task_3_0, auto_open=False)

        # Add auto page refresh to the HTML document.
        with open(file=self.path_html_task_3_0, mode='r+') as document_html:
            document_html_content = document_html.read()
            document_html_content = document_html_content.replace('<meta charset="utf-8" />',
                                                                  '<title>Graphs - Active clients</title>'
                                                                  '<meta http-equiv="refresh" content="60">')
            document_html.seek(0)
            document_html.write(document_html_content)
