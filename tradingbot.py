import os
import pandas as pd
import robin_stocks.robinhood as rs
from datetime import timedelta, datetime
import datetime as dt
import time
from time import sleep
import tradinghelpers
import yfinance as yf
from backtest import RSIBacktest
from backtest import MACDBacktest

stock = "NVDA"
#Fetch User and Pass

robinuser= os.environ.get("robinhood_username")
robinpass= os.environ.get("robinhood_password")

#Robinhood login
def login():
    rs.login(username="",
         password="",
         expiresIn=86400,
         by_sms=True)

#Robinhood Logout
def logout():
    rs.authentication.logout()

def get_stocks():
    stocks = ['NVDA', 'TSLA']
    return (stocks)

def market_open():
    market = False
    time_now = dt.datetime.now().time()

    mark_open = dt.time(8,30,0)
    mark_close = dt.time(14,59,0)

    if time_now > mark_open and time_now < mark_close:
        market = True
    else:
        print("Market is closed")
    return(market)

#login()
stocks = get_stocks()
print('stocks:', stocks)

while market_open():
    prices= rs.stocks.get_latest_price(stocks, 'ask_price')

    for i, stock in enumerate(stocks):
        price = float(prices[i])
        print('{} = ${}'.format(stock,price))

    break

RSI = tradinghelpers.rsigetter(stock)
# MACD = tradinghelpers.macdgetter(stock)
# VOLUME = tradinghelpers.volumeGetter(stock) 
# HIGHLOW = tradinghelpers.highlowGetter(stock)
# EARNINGSDATE = tradinghelpers.earningsGetter(stock)
# OPTIONSDATE = tradinghelpers.optionschainGetter(stock)

#MergedFrame = RSI2.merge(MACD2, on="Ticker").merge(VOLUME2,on="Ticker").merge(HIGHLOW2, on= "Ticker")
#print(MergedFrame)

stock = "NVDA"
RSItrade = RSIBacktest()
MACDtrade = MACDBacktest()

for i in stocks:
    RSItrade.rsi_backtest(i)
    MACDtrade.macd_backtest(i)