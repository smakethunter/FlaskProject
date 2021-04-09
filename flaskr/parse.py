import yfinance
import pandas as pd
import numpy as np
def compute_diff(data):

    avg_price = (data['Open']+ data['High'])/2
    data['AveragePrice'] = avg_price

    for interval in [1, 2, 5, 10, 20, 30]:
        data[f'Diff{interval}'] = data['AveragePrice'].pct_change(periods=interval)
    data['tomorrow'] = (-data['AveragePrice']+data['AveragePrice'].shift(periods=-1))/data['AveragePrice'].shift(periods=-1)
    data = data.dropna()
    return data

def get_historical_data(name_if_token: str):

    token = yfinance.Ticker(name_if_token)
    info = token.info['longBusinessSummary']
    print(info)

    data = token.history(period='max')

    data = data[['Open', 'Close', 'High', 'Low']]
    data['Date'] = data.index
    data = compute_diff(data)
    print(data.columns)
    return data