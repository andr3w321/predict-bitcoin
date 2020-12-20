import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
import pandas as pd

def graph_usdt_supply_vs_miner_revenue(df):
    df1 = df[df['Time'] >= '2017-01-01']
    df1["cumulative_MinerRevenue"] = df1["MinerRevenue"].cumsum()
    df1 = df1[["Time","USDT_supply","cumulative_MinerRevenue"]]
    ax = df1.set_index("Time").plot()

    plt.xlabel("Date")
    plt.ylabel("Dollars")
    plt.title("Bitcoin: cumulative USDT printed and cumulative mining revenue since 1/1/2017")
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # format y axis with commas
    #ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=4))
    plt.show()

def graph_usdt_supply_vs_usdt_marketcap(df):
    df1 = df[df['Time'] >= '2017-01-01']
    df1 = df1[["Time","USDT_marketcap","USDT_supply"]]
    ax = df1.set_index("Time").plot()

    plt.xlabel("Date")
    plt.ylabel("Dollars")
    plt.title("USDT_marketcap vs USDT_supply")
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # format y axis with commas
    #ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=4))
    plt.show()

def graph_usdt_price_vs_bfx_premium(df):
    df1 = df[df['Time'] >= '2017-01-01']
    df1 = df1[["Time","USDT_price","coinbase/bfx"]]
    ax = df1.set_index("Time").plot()

    plt.xlabel("Date")
    plt.ylabel("Dollars")
    plt.title("USDT_price vs coinbase/bitfinex price")
    #ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=4))
    plt.show()

df = pd.read_csv("./data/combined.csv")
#graph_usdt_supply_vs_miner_revenue(df)
#graph_usdt_supply_vs_usdt_marketcap(df)
graph_usdt_price_vs_bfx_premium(df)
