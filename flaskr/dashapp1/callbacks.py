from datetime import datetime as dt

import pandas_datareader as pdr
from dash.dependencies import Input
from dash.dependencies import Output
import datetime

def register_callbacks(dashapp):
    @dashapp.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value'),
                                                     Input('time-select', 'value')])
    def update_graph(selected_dropdown_value, selected_year):
        if selected_year == 0:
            start = dt(2017, 1, 1)
        else:
            start = dt.now()-datetime.timedelta(days=selected_year)
        df = pdr.get_data_yahoo(selected_dropdown_value, start=start, end=dt.now())
        print(selected_year)

        df = df.tail(selected_year)
        return {
            'data': [{
                'x': df.index,
                'y': df.Close
            }],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }