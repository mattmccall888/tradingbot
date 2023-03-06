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
    
    global rsiPeriod
    global rsiInterval
    finalframe = pd.DataFrame()
    templist = []
    stocklist = []
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
        templist.append(rsi[-1])
        stocklist.append(i)

    finalseries = pd.Series(templist, name='RSI') #Rsi values
    stockseries = pd.Series(stocklist, name = 'Ticker') #Tickers
    finalframe = pd.concat([stockseries, finalseries], axis=1)
    return(finalframe)

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

    global macdPeriod
    global macdInterval
    stocklist = []
    templist1 = []
    templist2 = []
    templist3 = []
    templist1_1 = []
    templist1_2 = []
    templist1_3 = []
    finalframe = pd.DataFrame()
    for i in stocks:
        # Request historic pricing data via finance.yahoo.com API
        df = yf.Ticker(i).history(period=macdPeriod)[['Close', 'Open', 'High', 'Volume', 'Low']]

        # Calculate MACD values using the pandas_ta library
        df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)

        # Creating Lists
        pd.set_option("display.max_columns", None)  # show all columns
        templist1 = df["MACD_12_26_9"].tolist()
        templist2 = df["MACDs_12_26_9"].tolist()
        templist3 = df["MACDh_12_26_9"].tolist()
        templist1_1.append(templist1[-1])
        templist1_2.append(templist2[-1])
        templist1_3.append(templist3[-1])
        stocklist.append(i)



    macdlist = pd.Series(templist1_1, name="MACD") #regular line
    macdslist = pd.Series(templist1_2, name="MACD-S") #signal line
    macdhlist = pd.Series(templist1_3, name="MACD-H") #difference between them, at 0 indicates a crossover
    stockseries = pd.Series(stocklist, name="Ticker")
    finalframe = pd.concat([stockseries, macdlist, macdslist, macdhlist], axis=1)
    return(finalframe)
    
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