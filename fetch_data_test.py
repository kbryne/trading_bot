import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Fetch data
stock = yf.Ticker("CRAYN.OL")
data = stock.history(start="2017-10-15", end="2024-07-15")


# Calculate RSI manually
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data


data = calculate_rsi(data)
data.dropna(inplace=True)

# Verify RSI calculation outside the strategy
print(data[['Close', 'RSI']].tail(20))


class RSIStrategy(Strategy):
    def init(self):
        self.rsi = self.I(lambda: self.data.RSI, name='RSI')

    def next(self):
        current_rsi = self.rsi[-1]
        last_rsi = self.rsi[-2]

        if self.position:
            if current_rsi > 70 and last_rsi <= 70:
                self.position.close()
        else:
            if current_rsi < 30 and last_rsi >= 30:
                self.buy()


# Perform the backtest
bt = Backtest(data, RSIStrategy, cash=10000, commission=0.002)
stats = bt.run()

# Plotting
plt.figure(figsize=(12, 8))

# Plot stock price
plt.plot(data.index, data['Close'], label='Close Price', color='blue')
plt.xlabel('Year')
plt.ylabel('Share price')
plt.title('Stock Price and RSI')

# Plot RSI
plt.twinx()  # Create a secondary y-axis for RSI
plt.plot(data.index, data['RSI'], label='RSI', color='red')
plt.axhline(30, color='blue', linestyle='--', label='Oversold (30)')
plt.axhline(70, color='blue', linestyle='--', label='Overbought (70)')
plt.ylabel('RSI')

# Adjust legend and layout
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

# Display backtest results
print(stats)
