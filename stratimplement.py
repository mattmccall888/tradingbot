#create a stock trading strategy and implement it

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import sched
import pandas_ta as pdt
from yahoo_fin.stock_info import get_data
import yahoo_fin.stock_info as si
import robin_stocks.robinhood as rs
import tradinghelpers

#Global Params for checks
enteredTrade = False
rsiPeriod = "1y"
rsiInterval = "1d"
macdPeriod = "1y"
macdInterval = "1d"

class RSIstrategy:
    def __init__(self, symbol, data, rsi_period=14, rsi_upper=70, rsi_lower=30):
        self.symbol = symbol
        self.data = data
        self.rsi_period = rsi_period
        self.rsi_upper = rsi_upper
        self.rsi_lower = rsi_lower
        
    def RSIgetter(self):
        delta = self.data['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=self.rsi_period).mean()
        avg_loss = loss.rolling(window=self.rsi_period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def generate_signals(self):
        # Get the RSI values for all previous days
        rsi = self.RSIgetter()
        
        # Generate the buy and sell signals
        signals = pd.DataFrame(index=self.data.index)
        signals['positions'] = np.where(rsi > self.rsi_upper, -1, np.where(rsi < self.rsi_lower, 1, 0))
        signals['positions'] = signals['positions'].diff()
        
        return signals
        
class MACDstrategy:
    def __init__(self, symbol, data, macd_fast=12, macd_slow=26, macd_signal=9):
        self.symbol = symbol
        self.data = data
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal
        
    def MACDgetter(self):
        macd = self.data.ta.macd(fast=self.macd_fast, slow=self.macd_slow, signal=self.macd_signal)
        return macd
    
    def generate_signals(self):
        # Get the MACD values for all previous days
        macd = self.MACDgetter()
        
        # Generate the buy and sell signals
        signals = pd.DataFrame(index=self.data.index)
        signals['positions'] = np.where(macd['MACD_12_26_9'] > macd['MACDh_12_26_9'], 1, np.where(macd['MACD_12_26_9'] < macd['MACDh_12_26_9'], -1, 0))
        signals['positions'] = np.where(macd['MACD_12_26_9'] < macd['MACDs_12_26_9'], 1, np.where(macd['MACD_12_26_9'] > macd['MACDs_12_26_9'], -1, 0))
        signals['positions'] = signals['positions'].diff()
        
        return signals
