import yfinance as yf
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import numpy as np
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG, SMA

# Fetch data
stock = yf.Ticker("CRAYN.OL")
data = stock.history(period="max")

# append rsi to dataframe
data['RSI_14'] = ta.rsi(data['Close'], length=14)

# Plotting
data['Buy'] = (data['RSI_14'] < 30) & (data['RSI_14'].shift(1) >= 30)
data['Sell'] = (data['RSI_14'] > 70) & (data['RSI_14'].shift(1) <= 70)

plt.figure(figsize=(12, 8))

# Plot stock price
plt.plot(data.index, data['Close'], label='Close Price', color='blue')
plt.xlabel('Year')
plt.ylabel('Share price')
plt.title('Stock Price and RSI')

# Plot RSI
plt.twinx()  # Create a secondary y-axis for RSI
plt.plot(data.index, data['RSI_14'], label='RSI', color='red')
plt.axhline(30, color='blue', linestyle='--', label='Oversold (30)')
plt.axhline(70, color='blue', linestyle='--', label='Overbought (70)')
plt.ylabel('RSI')

# Plot buy and sell signals on stock price plot
plt.scatter(data.index[data['Buy']], data['Close'][data['Buy']],
            marker='^', color='green', label='Buy Signal')
plt.scatter(data.index[data['Sell']], data['Close'][data['Sell']],
            marker='v', color='red', label='Sell Signal')

# Adjust legend and layout
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

# Backtesting

stock = yf.Ticker("CRAYN.OL")
data = stock.history(period="max")
data['RSI_14'] = ta.rsi(data['Close'], length=14)


class RSI(Strategy):
    def init(self):
        self.rsi = self.I(ta.rsi, self.data.Close, 14)
        print(self.rsi)
    def next(self):
        current_rsi = self.rsi[-1]
        last_rsi = self.rsi[-2]
        if current_rsi > 70 and last_rsi <= 70:
            self.sell()
        elif current_rsi < 30 and last_rsi >= 30:
            self.buy()

bt = Backtest(data, RSI, cash=10000, commission=0.002)
stats = bt.run()


plt.figure(figsize=(12, 8))

# Plot stock price
plt.plot(data.index, data['Close'], label='Close Price', color='blue')
plt.xlabel('Year')
plt.ylabel('Share price')
plt.title('Stock Price and RSI')

# Plot RSI
plt.twinx()  # Create a secondary y-axis for RSI
plt.plot(data.index, data['RSI_14'], label='RSI', color='red')
plt.axhline(30, color='blue', linestyle='--', label='Oversold (30)')
plt.axhline(70, color='blue', linestyle='--', label='Overbought (70)')
plt.ylabel('RSI')

# Adjust legend and layout
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

# Display backtest results
print(stats)

