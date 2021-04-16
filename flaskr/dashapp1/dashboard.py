"""Instantiate a Dash app."""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
from .data import register_callbacks

from .layout import html_layout
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
import plotly.graph_objects as go
def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/"

    )
    register_callbacks(dashapp=dash_app)

    # Load DataFrame
    #df = create_dataframe()
    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div([html.Div(
        children=[
    html.H1('Stock Price Prediction'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Coke', 'value': 'COKE'},
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Apple', 'value': 'AAPL'},
            {'label': 'Facebook', 'value': 'FB'},
            {'label': 'Amazon', 'value': 'AMZN'},
            {'label': 'Netflix', 'value': 'NFLX'},
            {'label': 'Google/Alphabet', 'value': 'GOOG'},
            {'label': 'Bitcoin', 'value': 'BTC'},
            {'label': 'Intel', 'value': 'INTC'}
        ],

        value='COKE'
    ),
    html.Br(),
    html.Br(),
    dcc.RadioItems(
        id='time-select',
        options=[{'label': i, 'value': k} for i, k in [('All Time', 0), ('Last Month', 30), ('Last Week', 7)]],
        value=30,
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id='my-graph'),
    html.Br(),
    html.Div(id = 'my-table')


    ],


        style={'width': '500'},

    ),
    # html.Div(id = 'table',
    #     children=[
    #         dash_table.DataTable(id="database-table",
    #                              columns=[
    #                                  'Date', 'AveragePrice', 'Diff1', 'tomorrow'
    #                              ],
    #                              page_current=0,
    #                              ),
    #
    #
    #     ]
    #
    # )

    ]

    )

    return dash_app.server



