import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from kraken_api_utils import *
from trading_metrics import CryptoCurrencyDF


def get_input():
    currency = st.sidebar.selectbox("Cripto Currency-Euro Pair:", get_euro_pairs())
    start_date = st.sidebar.date_input("Start Date", datetime(2022, 7, 1))
    granularity = st.sidebar.selectbox("Granularity:", ("hourly", "daily", "weekly"))
    metric = st.sidebar.selectbox("Moving Average Metric:", ("SMA10", "SMA20", "SMA50", "EMA10", "EMA20", "EMA50"))
    return currency, start_date, granularity, metric


if __name__ == '__main__':
    st.write(''' # Cryptocurrency Dashboard Application: 
    Choose a currency from the list (pairs available at KrakenAPI) to visualize its price (euro) for the desired time period.\
    You can choose between the following metrics: 
    * **SMA10/20/30**: Simple moving average of the last 10/20/30 days, hours or weeks
    * **EMA10/20/30**: Exponential moving average of the last 10/20/30 days, hours or weeks
                  
    For daily data, the **RSI** indicator is also calculated''')
    image = Image.open("Crypto_Graphics\dashboard_image.jpg")
    st.image(image, use_column_width=True)

    st.sidebar.header('User Input')

    currency, start_date, granularity, metric = get_input()
    data_df = CryptoCurrencyDF(get_OHLC_data(euro_pair=currency, since=start_date, granularity=granularity))

    # Calculate selected metric:
    if metric == "SMA10":
        data_df.SMA10()
    elif metric == "SMA20":
        data_df.SMA20()
    elif metric == "SMA50":
        data_df.SMA50()
    elif metric == "EMA10":
        data_df.EMA10()
    elif metric == "EMA20":
        data_df.EMA20()
    elif metric == "EMA50":
        data_df.EMA50()
    else:
        raise ValueError('Metric not Available')

    fig1 = go.Figure(
        data=[go.Candlestick(
            x=data_df['datetime'],
            open=data_df['open'],
            high=data_df['high'],
            low=data_df['low'],
            close=data_df['close'],
            increasing_line_color='green',
            decreasing_line_color='red',
            name='OHLC'
        )]
    )
    metric_trace = go.Scatter(x=data_df['datetime'], y=data_df[metric], mode='lines', name=metric)
    fig1.add_trace(metric_trace)

    # We print CandleStick Graph
    st.header(currency + " CandleStick Graph")
    st.plotly_chart(fig1)

    # We print RSI: (for daily data)
    if granularity == 'daily':
        # Calculate RSI:
        data_df.RSI()
        st.header(currency + " RSI Graph")
        fig2 = go.Figure(
            data=[go.Scatter(x=data_df['datetime'], y=data_df['RSI'], mode='markers+lines', name='RSI')])
        st.plotly_chart(fig2)

    # We print the data
    st.header(currency + " Data:")
    st.write(data_df)




