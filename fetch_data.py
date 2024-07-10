import yfinance as yf
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import numpy as np

# tester ut yfinance
norsk_hydro = yf.Ticker("NHY.OL")
info = norsk_hydro.info
data_hist = norsk_hydro.history(period="max")
metadata = norsk_hydro.history_metadata
div_n_splits =norsk_hydro.actions
div = norsk_hydro.dividends
splits = norsk_hydro.splits
income_statement = norsk_hydro.income_stmt
quarterly_income_statement = norsk_hydro.quarterly_income_stmt
balance = norsk_hydro.balance_sheet
quarterly_balance = norsk_hydro.quarterly_balance_sheet
cashflow = norsk_hydro.cashflow
quarterly_cashflow = norsk_hydro.quarterly_cashflow
share_holders = norsk_hydro.major_holders
mutual_fund_holders = norsk_hydro.mutualfund_holders
insider_trades = norsk_hydro.insider_purchases
insider_transactions = norsk_hydro.insider_transactions
insiders = norsk_hydro.insider_roster_holders
recommendations = norsk_hydro.recommendations
recommendations_sum = norsk_hydro.recommendations_summary
upgrades_downgrades = norsk_hydro.upgrades_downgrades
earnings_dates = norsk_hydro.earnings_dates
isin = norsk_hydro.isin
options = norsk_hydro.options
news = norsk_hydro.news
share_count = norsk_hydro.get_shares_full(start="1900-01-01", end="2100-01-01")

# Technical analysis
stock = yf.Ticker("ELMRA.OL")
data = stock.history(period="max")

# append because
data_rsi = data.ta.rsi(close="close", length=14, append=True)

# print(data[['Close', 'RSI_14']])
data['Buy'] = (data['RSI_14'] < 30) & (data['RSI_14'].shift(1) >= 30)
data['Sell'] = (data['RSI_14'] > 70) & (data['RSI_14'].shift(1) <= 70)



# Plotting
plt.figure(figsize=(12, 8))

# Plot stock price
plt.plot(data.index, data['Close'], label='Close Price', color='blue')
plt.xlabel('Year')
plt.ylabel('Share price')
plt.title('Elmera group - Stock Price and RSI')

# Plot RSI
plt.twinx()  # Create a secondary y-axis for RSI
plt.plot(data.index, data['RSI_14'], label='RSI', color='red')
plt.axhline(30, color='blue', linestyle='--', label='Oversold (30)')
plt.axhline(70, color='blue', linestyle='--', label='Overbought (70)')
plt.ylabel('RSI')

# Plot buy and sell signals on stock price plot
plt.scatter(data.index[data['Buy']], data['Close'][data['Buy']], marker='^', color='green', label='Buy Signal')
plt.scatter(data.index[data['Sell']], data['Close'][data['Sell']], marker='v', color='red', label='Sell Signal')

# Adjust legend and layout
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

#%%

# One plot

plt.figure(figsize=(12, 8))

# Plot stock price
plt.plot(data.index, data['Close'])
plt.xlabel('Year')
plt.ylabel('Share price/RSI value')
plt.title('Crayon')

# Plot RSI
plt.plot(data.index, data['RSI_14'])
plt.axhline(30, color='blue')
plt.axhline(70, color='blue')

# Plot buy and sell indicator
plt.scatter(data.index[data['Buy']], data['RSI_14'][data['Buy']], marker='^', color='green')
plt.scatter(data.index[data['Sell']], data['RSI_14'][data['Sell']], marker='v', color='red')
plt.show()
#%%