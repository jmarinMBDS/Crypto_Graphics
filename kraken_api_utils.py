import requests
import pandas as pd
from datetime import datetime, time
import calendar


def get_euro_pairs():
    '''Obtains a list of all available currencies on the Kraken API over Euro'''
    resp = requests.get('https://api.kraken.com/0/public/AssetPairs')
    resp = resp.json()

    euro_pairs = []
    for pair in resp['result']:
        if pair.endswith('EUR'):
            euro_pairs.append(pair)
    return euro_pairs


def get_OHLC_data(euro_pair='ETHWEUR', since=datetime(2022, 7, 1),  granularity='daily'):
    '''Obtains OHLC data for the given currency since start_date in intervals of weeks, days or hours'''

    # Convert start_date to unixtimestamp format
    since = datetime.combine(since, time())
    unix_timestamp = calendar.timegm(since.utctimetuple())

    # Define interval (minutes):
    if granularity == 'hourly':
        interval = 60
    elif granularity == 'daily':
        interval = 1440
    elif granularity == 'weekly':
        interval = 10080
    else:
        raise ValueError("Metric not available")

    # Build request:
    endpoint = 'https://api.kraken.com/0/public/OHLC'
    payload = {
        'pair': euro_pair,
        'interval': interval,
        'since': unix_timestamp
    }
    resp = requests.get(endpoint, payload)

    ohlc_data = pd.DataFrame(resp.json()['result'][euro_pair])
    ohlc_data.columns = ['unixtimestamp', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']

    ohlc_data['datetime'] = pd.to_datetime(ohlc_data['unixtimestamp'], unit='s')

    #we select only columns of interest:
    ohlc_data = ohlc_data.loc[:, ['datetime','open', 'high', 'low', 'close']]
    cols = ohlc_data.columns.drop('datetime')
    ohlc_data[cols] = ohlc_data[cols].apply(pd.to_numeric, errors='coerce')

    return ohlc_data

