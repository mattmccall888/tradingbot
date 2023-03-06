import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from stratimplement import RSIstrategy
import yfinance as yf
import pandas_ta as pdt
from stratimplement import MACDstrategy

# Set the global parameters for all tests
rsiPeriod = "1y"
rsiInterval = "1d"
rsi_period = 14
rsi_upper = 70
rsi_lower = 30
macdPeriod = "1y"
macdInterval = "1d"


class RSIBacktest:
    def rsi_backtest(self, stock):
    # Load price data for the stock from Yahoo Finance
        symbol = yf.Ticker(stock)
        df_stock = symbol.history(interval= rsiInterval ,period= rsiPeriod)

        # Instantiate the RSI strategy object
        rsi_strategy = RSIstrategy('AAPL', df_stock)

        # Generate signals
        signals_df = rsi_strategy.generate_signals()

        # Combine price and signal dataframes
        data_df = pd.concat([df_stock , signals_df], axis=1)

        # Backtest the strategy
        data_df['positions'] = data_df['positions'].shift(1)
        data_df['returns'] = np.log(data_df['Close'] / data_df['Close'].shift(1))
        data_df['strategy_returns'] = data_df['returns'] * data_df['positions']
        cumulative_strategy_returns = np.exp(data_df['strategy_returns'].cumsum())
        #Turn into a percentage
        cumulative_strategy_returns = (cumulative_strategy_returns * 100) -100

        # Plot the backtested strategy returns
        fig, ax = plt.subplots(figsize=(10, 5))
        cumulative_strategy_returns.plot(ax=ax)
        ax.set_xlabel('Date')
        ax.set_ylabel('Cumulative Strategy Returns in %')
        ax.set_title('Backtesting RSI Strategy on ' + stock + ' RSI Period: ' + rsiPeriod + ' RSI Interval: ' + rsiInterval)
        plt.show()

class MACDBacktest:
    def macd_backtest(self, stock):
    # Load price data for the stock from Yahoo Finance
        symbol = yf.Ticker(stock)
        df_stock = symbol.history(interval= macdInterval ,period= macdPeriod)

        # Instantiate the RSI strategy object
        macd_strategy = MACDstrategy('AAPL', df_stock)

        # Generate signals
        signals_df = macd_strategy.generate_signals()

        # Combine price and signal dataframes
        data_df = pd.concat([df_stock , signals_df], axis=1)

        # Backtest the strategy
        data_df['positions'] = data_df['positions'].shift(1)
        data_df['returns'] = np.log(data_df['Close'] / data_df['Close'].shift(1))
        data_df['strategy_returns'] = data_df['returns'] * data_df['positions']
        cumulative_strategy_returns = np.exp(data_df['strategy_returns'].cumsum())
        #Turn into a percentage
        cumulative_strategy_returns = (cumulative_strategy_returns * 100) -100

        # Plot the backtested strategy returns
        fig, ax = plt.subplots(figsize=(10, 5))
        cumulative_strategy_returns.plot(ax=ax)
        ax.set_xlabel('Date')
        ax.set_ylabel('Cumulative Strategy Returns in %')
        ax.set_title('Backtesting MACD Strategy on ' + stock + ' MACD Period: ' + macdPeriod + ' MACD Interval: ' + macdInterval)
        plt.show()