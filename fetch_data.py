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

data['Buy'] = (data['RSI'] < 30) & (data['RSI'].shift(1) >= 30)
data['Sell'] = (data['RSI'] > 70) & (data['RSI'].shift(1) <= 70)

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

# Plot buy and sell signals on stock price plot
plt.scatter(data.index[data['Buy']], data['Close'][data['Buy']],
            marker='^', color='green', label='Buy Signal')
plt.scatter(data.index[data['Sell']], data['Close'][data['Sell']],
            marker='v', color='red', label='Sell Signal')

# Adjust legend and layout
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

# Display backtest results
print(stats)

# testing yfinance
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

