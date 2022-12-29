import pandas as pd
pd.options.mode.chained_assignment = None
from kraken_api_utils import *
# We define the class CryptoCurrency in order to add new methods to pandas dataframe
# for calculating different trading metrics


class CryptoCurrencyDF(pd.DataFrame):

    @property
    def _constructor(self):
        return CryptoCurrencyDF

    def SMA10(self):
        self['SMA10'] = self['close'].rolling(10).mean()
        return self

    def SMA20(self):
        self['SMA20'] = self['close'].rolling(20).mean()
        return self

    def SMA50(self):
        self['SMA50'] = self['close'].rolling(50).mean()
        return self

    def EMA10(self):
        self['EMA10'] = self['close'].ewm(span=10).mean()
        return self

    def EMA20(self):
        self['EMA20'] = self['close'].ewm(span=20).mean()
        return self

    def EMA50(self):
        self['EMA50'] = self['close'].ewm(span=50).mean()
        return self

    def RSI(self):

        self['diff'] = self['close'].diff()
        self['gain'] = self['diff'].clip(lower=0).round(2)
        self['loss'] = self['diff'].clip(upper=0).abs().round(2)

        # calculate first SMA value
        window_length = 14
        self['avg_gain'] = self['gain'].rolling(window=window_length,
                                                min_periods=window_length).mean()[:window_length + 1]
        self['avg_loss'] = self['loss'].rolling(window=window_length,
                                                min_periods=window_length).mean()[:window_length + 1]

        # Get WMS averages
        # Average Gains
        for i, row in enumerate(self['avg_gain'].iloc[window_length + 1:]):
            self['avg_gain'].iloc[i + window_length + 1] = \
                (self['avg_gain'].iloc[i + window_length] *
                 (window_length - 1) +
                 self['gain'].iloc[i + window_length + 1]) / window_length

        # Average Losses
        for i, row in enumerate(self['avg_loss'].iloc[window_length + 1:]):
            self['avg_loss'].iloc[i + window_length + 1] = \
                (self['avg_loss'].iloc[i + window_length] *
                 (window_length - 1) +
                 self['loss'].iloc[i + window_length + 1]) / window_length

        # Calculate RS Values
        self['rs'] = self['avg_gain'] / self['avg_loss']
        # Calculate RSI
        self['RSI'] = 100 - (100 / (1.0 + self['rs']))
        return self



