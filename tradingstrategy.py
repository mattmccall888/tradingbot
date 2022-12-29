import pandas as pd
import robin_stocks as rs
import robin_stocks.helper as helper
import robin_stocks.urls as url

def spreadcriteriacheck(stocks):
    goodstocks = []
    stocks = stocks
    for i in stocks:
        print(rs.robinhood.stocks.get_earnings(i))
    
