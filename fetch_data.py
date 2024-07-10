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
stock = yf.Ticker("NHY.OL")
data = stock.history(period="max")
data_rsi = data.ta.rsi()
print(data_rsi)


