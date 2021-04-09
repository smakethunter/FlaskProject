
from datetime import datetime as dt

import pandas_datareader as pdr
from dash.dependencies import Input
from dash.dependencies import Output
from flaskr.parse import compute_diff
import pandas as pd
import tensorflow as tf
import dash_table
import datetime
from datetime import date
def register_callbacks(dashapp):
    @dashapp.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value'), Input('time-select', 'value')])
    def update_graph(selected_dropdown_value, selected_period):

        df = pdr.get_data_yahoo(selected_dropdown_value, start=dt(2017, 1, 1), end=dt.now())

        data = compute_diff(df)
        model = tf.keras.models.load_model('/Users/smaket/PycharmProjects/flaskProject/flaskr/my_model')
        #model.fit(data[['Diff1', 'Diff2', 'Diff5']].values,data['tomorrow'].values, batch_size=32, epochs=10)

        tomorrow = model.predict(data[['Diff1', 'Diff2', 'Diff5']].tail(1).values)[0, 0]
        tomorrow = float(round(tomorrow, 2))
        #print(tomorrow)
        sign = '' if tomorrow <= 0 else '+'
        return {
            'data': [{
                'x': data.index[selected_period:] if selected_period > 0 else df.index ,
                'y': data.AveragePrice.tail(selected_period) if selected_period > 0 else df.AveragePrice
            }],

            'layout': {
                'title': "Tomorrow's Forecast {}{:.2f}".format(sign, tomorrow),
                # 'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}
            }
        }
    @dashapp.callback(Output("database-table", 'data' ), [Input('my-dropdown', 'value')])

    def create_data_table(selected_dropdown_value):
        """Create Dash datatable from Pandas DataFrame."""
        df = pdr.get_data_yahoo(selected_dropdown_value, start=dt(2017, 1, 1), end=dt.now())
        df = compute_diff(df)
        df['Date'] = df.index.strftime('%d-%m-%Y')
        print(df[[ 'AveragePrice', 'Diff1', 'tomorrow']].tail(14))
        table = df[[ 'AveragePrice', 'Diff1', 'tomorrow']].tail(14).to_dict('records') #if selected_period > 0 else df[['Date','AveragePrice', 'Diff1', 'tomorrow']][:].to_dict("records")
        print(table)
        return table


