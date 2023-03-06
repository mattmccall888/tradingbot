import pandas as pd
import robin_stocks as rs
import robin_stocks.helper as helper
import robin_stocks.urls as url
from datetime import timedelta, datetime
import datetime as dt
from datetime import datetime
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import sched
import pandas_ta as pdt
from yahoo_fin.stock_info import get_data
import yahoo_fin.stock_info as si

#Global Params for checks
enteredTrade = False
rsiPeriod = "1y"
rsiInterval = "1d"
macdPeriod = "1y"
macdInterval = "1d"

def SMAgetter(stock, period, interval):
    symbol = yf.Ticker(stock)
    df_stock = symbol.history(interval= interval ,period= period)
    df_stock.ta.sma(close='close', length=20, append=True)
    sma = df_stock["SMA_20"].tolist()
    return(sma)

def rsigetter(stock):
    global rsiPeriod
    global rsiInterval
    symbol = yf.Ticker(stock)
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
    return(rsi)

def macdgetter(stock):
    global macdPeriod
    global macdInterval
    symbol = yf.Ticker(stock)
    df_stock = symbol.history(interval= macdInterval ,period= macdPeriod)

    #print(df_stock)
    df_stock.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
    macd = df_stock["MACD_12_26_9"].tolist()
    macds = df_stock["MACDs_12_26_9"].tolist()
    macdh = df_stock["MACDh_12_26_9"].tolist()
    return(macd + macds + macdh)
    
def volumeGetter(stock):
    symbol = yf.Ticker(stock)
    currVol = (symbol.info["averageVolume10days"])
    return(currVol)

def highlowGetter(stock):
    symbol = yf.Ticker(stock)
    yearhigh = (symbol.info["fiftyTwoWeekHigh"])
    yearlow = (symbol.info["fiftyTwoWeekLow"])
    dayhigh = (symbol.info["dayHigh"])
    daylow = (symbol.info["dayLow"])
    return(yearhigh, yearlow, dayhigh, daylow)

#Fetch last x years of earnings dates for a single ticker
def earningsGetter(years, stock):
    earningslist = []
    stock = yf.Ticker(stock)
    finalframe = pd.DataFrame()
    dateframe = pd.DataFrame()
    for i in years:
        earningslist.append(i)
        df = pd.DataFrame()
        df[i] = stock.earnings_dates.index
        dateframe = pd.concat([df[i]], axis = 1)
    #stockseries = pd.Series(stocklist, name="Ticker")
    finalframe = pd.concat([dateframe], axis=1)
    return (finalframe)

def earningsGetter(stocks):
    earningslist = []
    stocklist = []
    finalframe = pd.DataFrame()
    dateframe = pd.DataFrame()
    for i in stocks:
        stocklist.append(i)
        currticker = yf.Ticker(i)
        df = pd.DataFrame()
        df[i] = currticker.earnings_dates.index
        dateframe = pd.concat([df[i]], axis = 1)
    #stockseries = pd.Series(stocklist, name="Ticker")
    finalframe = pd.concat([dateframe], axis=1)
    return (finalframe)

def optionschainGetter(stock):
    earningslist = []
    stocklist = []
    finalframe = pd.DataFrame()
    dateframe = pd.DataFrame()
    for i in stock:
        stocklist.append(i)
        currticker = yf.Ticker(i)
        df = pd.DataFrame()
        df[i] = currticker.options
        dateframe = pd.concat([df[i]], axis = 1)
    #stockseries = pd.Series(stocklist, name="Ticker")
    finalframe = pd.concat([dateframe], axis=1)
    return (finalframe)