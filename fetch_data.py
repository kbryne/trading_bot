import yfinance as yf
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import numpy as np

norsk_hydro = yf.Ticker("NHY.OL")
info = norsk_hydro.info
data_hist = norsk_hydro.history(period="max")
metadata = norsk_hydro.history_metadata
# dividends and stock splits
div_n_splits =norsk_hydro.actions
div = norsk_hydro.dividends
splits = norsk_hydro.splits
# share count
share_count = norsk_hydro.get_shares_full(start="1900-01-01", end="2100-01-01")
print(share_count)


