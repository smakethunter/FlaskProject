"""Plotly Dash HTML layout override."""

html_layout = """
<!DOCTYPE html>
    <html>
        <title>Stock Prediction</title>

<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<link href="../static/bootstrap-5.0.0-beta3-examples/assets/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="../static/bootstrap-5.0.0-beta3-examples/dashboard/dashboard.css" rel="stylesheet">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="Mark Otto, Jacob Thornton, and Bootstrap contributors">
    <meta name="generator" content="Hugo 0.82.0">
    <title>Dashboard Template · Bootstrap v5.0</title>

    <link rel="canonical" href="https://getbootstrap.com/docs/5.0/examples/dashboard/">



    <!-- Bootstrap core CSS -->
<link href="../static/bootstrap-5.0.0-beta3-examples/assets/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }
    </style>


    <!-- Custom styles for this template -->
    <link href="../static/bootstrap-5.0.0-beta3-examples/dashboard/dashboard.css" rel="stylesheet">
  </head>
        <header class="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-0 shadow">
  <a class="navbar-brand col-md-3 col-lg-2 me-0 px-3" href="/">MLDemo</a>

            <a class="nav-link" href="/ml_api/selection">
              <span data-feather="file"></span>
              Prediction model
            </a>

  <ul class="navbar-nav px-3">
      <li class="nav-item text-nowrap"><a class="nav-link" href="/ml_api/services/1">Back</a>    
  </ul>
</header>

            </header>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
"""

"""
import dash_core_components as dcc
import dash_html_components as html

layout = html.Div([
    html.H1('Stock Tickers'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Coke', 'value': 'COKE'},
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Apple', 'value': 'AAPL'}
        ],
        value='COKE'
    ),
    dcc.Graph(id='my-graph')
], style={'width': '500'})
"""