import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from datetime import date as date_class
from datetime import timedelta, datetime
from matplotlib.ticker import PercentFormatter

df = pd.read_csv(r'/home/anto/Documents/Coding/fred_graph/data_27_05_2021.csv')
# plot original data from FRED
df = df[df.RRPONTSYD != "."]
X = [dt.datetime.strptime(value[0], "%Y-%m-%d") for value in df.values]
Y = [float(value[1]) for value in df.values]
plt.plot(X, Y)
plt.xlabel("date")
plt.gcf().autofmt_xdate()
plt.ylabel("RRPONTSYD")
plt.title("Overnight Reverse Repurchase Agreements")
plt.show()
