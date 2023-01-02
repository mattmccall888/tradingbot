import pandas as pd
import robin_stocks as rs
import robin_stocks.helper as helper
import robin_stocks.urls as url
from datetime import timedelta, datetime
import datetime as dt
from pyrh import Robinhood
from datetime import datetime
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import sched
import pandas_ta as pdta

#Global Params for checks
enteredTrade = False
rsiPeriod = "1y"
rsiInterval = "1d"
macdPeriod = "1y"
macdInterval = "1d"


def rsicheck(stocks):
    global rsiPeriod
    global rsiInterval
    finallist = []
    for i in stocks:
        symbol = yf.Ticker(i)
        df_stock = symbol.history(interval= rsiInterval ,period= rsiPeriod)

        #print(df_stock)
        change = df_stock["Close"].diff()
        change.dropna(inplace=True)
        # Create two copies of the Closing price Series
        change_up = change.copy()
        change_down = change.copy()

        # 
        change_up[change_up<0] = 0
        change_down[change_down>0] = 0

        # Verify that we did not make any mistakes
        change.equals(change_up+change_down)

        # Calculate the rolling average of average up and average down
        avg_up = change_up.rolling(14).mean()
        avg_down = change_down.rolling(14).mean().abs()

        rsi = 100 * avg_up / (avg_up + avg_down)

        #print(rsi)

        #Take a look at the 20 oldest datapoints
        

        # Set the theme of our chart
        plt.style.use('fivethirtyeight')

        # Make our resulting figure much bigger
        plt.rcParams['figure.figsize'] = (20, 20)

        # Create two charts on the same figure.
        ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
        ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)

        # First chart:
        # Plot the closing price on the first chart
        ax1.plot(df_stock['Close'], linewidth=2)
        ax1.set_title(i + ' Close Price')

        # Second chart
        # Plot the RSI
        ax2.set_title('Relative Strength Index')
        ax2.plot(rsi, color='orange', linewidth=1)
        # Add two horizontal lines, signalling the buy and sell ranges.
        # Oversold
        ax2.axhline(30, linestyle='-', linewidth=1.5, color='green')
        # Overbought
        ax2.axhline(70, linestyle='-', linewidth=1.5, color='red')

        #plt.show()
        finallist.append(rsi[-1])
    return(finallist)

def macdcheck(stocks):
    global macdPeriod
    global macdInterval
    finallist = []
    for i in stocks:
        # Request historic pricing data via finance.yahoo.com API
        df = yf.Ticker(i).history(period=macdPeriod)[['Close', 'Open', 'High', 'Volume', 'Low']]

        # Calculate MACD values using the pandas_ta library
        df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)

        # View result
        pd.set_option("display.max_columns", None)  # show all columns
        print(df)
    
