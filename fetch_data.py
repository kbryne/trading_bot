#%%
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import numpy as np
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Fetch data
stock = yf.Ticker("CRAYN.OL")
data = stock.history(period="max")

# append rsi to dataframe
data['RSI_14'] = ta.rsi(data['Close'], length=14)

# Drop NaN values in RSI_14 column
# data.dropna(subset=['RSI_14'], inplace=True)

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
class RSIStrategy(Strategy):
    def init(self):
        # checking RSI values
        self.rsi = self.data['RSI_14']

    def next(self):
        # print current rsi
        print(f"Current RSI: {self.rsi[-1]}")

        if self.rsi[-1] < 30 and self.rsi[-2] >= 30:
            print("RSI crossed below 30, buy")
            self.buy()
        elif self.rsi[-1] > 70 and self.rsi[-2] <= 70:
            print("RSI crossed above 70, sell")
            self.sell()



bt = Backtest(data, RSIStrategy, cash=10000, commission=0.002)
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

# Plot buy and sell signals based on hypothetical _Stats structure
if hasattr(stats, 'closed_trades') and len(stats.closed_trades) > 0:
    for trade in stats.closed_trades:
        if trade.type == 'buy':
            plt.scatter(trade.exit_date, trade.exit_price, marker='^', color='green', label='Buy Signal')
        elif trade.type == 'sell':
            plt.scatter(trade.exit_date, trade.exit_price, marker='v', color='red', label='Sell Signal')

# Adjust legend and layout
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

# Display backtest results
print(stats)






# tester ut yfinance
stock = yf.Ticker("NHY.OL")
info = stock.info
data_hist = stock.history(period="max")
metadata = stock.history_metadata
div_n_splits =stock.actions
div = stock.dividends
splits = stock.splits
income_statement = stock.income_stmt
quarterly_income_statement = stock.quarterly_income_stmt
balance = stock.balance_sheet
quarterly_balance = stock.quarterly_balance_sheet
cashflow = stock.cashflow
quarterly_cashflow = stock.quarterly_cashflow
share_holders = stock.major_holders
mutual_fund_holders = stock.mutualfund_holders
insider_trades = stock.insider_purchases
insider_transactions = stock.insider_transactions
insiders = stock.insider_roster_holders
recommendations = stock.recommendations
recommendations_sum = stock.recommendations_summary
upgrades_downgrades = stock.upgrades_downgrades
earnings_dates = stock.earnings_dates
isin = stock.isin
options = stock.options
news = stock.news
share_count = stock.get_shares_full(start="1900-01-01", end="2100-01-01")
