import sys
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
df = pd.read_csv(r'/home/anto/Documents/Coding/fred_graph/data.csv')

df = df[df.RRPONTSYD != "."]
"""
scatter = go.Scatter(x=df["DATE"], y=df["RRPONTSYD"], name="Billions USD")
fig = go.Figure()
fig.add_trace(trace=scatter)
fig.update_layout(title="Overnight Reverse Repurchase Agreements", plot_bgcolor="rgb(230,230,230)", showlegend=True)
fig.show()
"""

X = [value[0] for value in df.values]
Y = [float(value[1]) for value in df.values]
plt.plot(X, Y)
plt.xlabel("date")
plt.gcf().autofmt_xdate()
plt.ylabel("RRPONTSYD")
plt.title("Overnight Reverse Repurchase Agreements")
plt.show()

"""
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv")
X = [value[0] for value in df.values]
Y = [value[1] for value in df.values]
plt.plot(X, Y)
plt.xlabel("date")
plt.gcf().autofmt_xdate()
plt.ylabel("AAPL share price")
plt.title("AAPL price over time")

plt.show()
"""

