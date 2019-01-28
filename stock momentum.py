#This code performs a backtesting of a return momentum strategy for a time series.
#Disclosure: Nothing in this repository should be considered investment advice. Past performance is not necessarily indicative of future returns.
# These are general examples about how to import data using pandas for a small sample of financial data across different time intervals.
#Please note that the below code is written with the objective to explore various python features.

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import quandl
import pandas as pd
import seaborn as sns
sns.set()

#Download data from Quandl
quandl.ApiConfig.api_key = "youquandlapikey"
today_date = date.today() - relativedelta(days=1)
data = quandl.get("NASDAQOMX/NDX.1", start_date="2018-06-04", end_date=today_date)

#Calculate one day return in dataframe
data['returns'] = np.log(data['Index Value'] / data['Index Value'].shift(1))


cols = []
#Calculate sign of rolling mean over predefined momentum period in new columns in dataframe
for momentum in [5, 10, 15, 20]:
    col = 'position_%s' % momentum

    data[col] = np.sign(data['returns'].rolling(momentum).mean())

    cols.append(col)

strats = ['returns']
stratdiffs =[]
#Calculate return based on sign of rolling mean, essentially going long or short depending on momentum
for col in cols:
    strat = 'strategy_{}s' .format(col.split('_')[1])
    data[strat] = data[col].shift(1) * data['returns']
    strats.append(strat)

    stratdiff = 'strategydiff_{}s' .format(col.split('_')[1])
    data[stratdiff] = (data[col].shift(1) * data['returns']) - data['returns']
    stratdiffs.append(stratdiff)

data[strats].dropna().cumsum().apply(np.exp).plot()
data[stratdiffs].dropna().cumsum().apply(np.exp).plot()

plt.show()