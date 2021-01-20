import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
#from combine-data import add_trailing column, add_forward_column

def get_bitcoinity_exchanges():
    return ["bitfinex","bitstamp","coinbase","kraken","gemini","mtgox","bit-x","cex.io","exmo"]#,"cdd_binance"]

def get_cdd_exchanges():
    return ["cdd_bitfinex","cdd_bitstamp","cdd_binance","cdd_kraken","cdd_bittrex","cdd_poloniex"]#,"cdd_itbit"]#,"cdd_gemini"]

def print_exchange_data_start_stop_dates(df, exchanges):
    for exchange in exchanges:
        if exchange in df.columns:
            start_date = df["Time"][df[exchange].first_valid_index()]
            stop_date = df["Time"][df[exchange].last_valid_index()]
            print("{},{},{}".format(exchange, start_date, stop_date))

def graph_usdt_supply_vs_miner_revenue(df):
    df1 = df[df['Time'] >= '2020-12-01'].copy()
    new_col = "Cumulative Miner Revenue"
    df1[new_col] = df1["MinerRevenue"].cumsum()
    df1 = df1[["Time","USDT_supply", new_col]]
    df1 = df1.reset_index()
    df1["USDT_supply"] = df1["USDT_supply"] - df1["USDT_supply"][0]
    fig, axes = plt.subplots(nrows=1, ncols=1, squeeze=False, figsize=(12,8))
    df1 = df1.set_index("Time")

    axes[0,0].plot(df1.index, df1[new_col], color='orange')
    axes[0,0].plot(df1.index, df1["USDT_supply"], color='blue')

    plt.xlabel("Date")
    plt.ylabel("Dollars")
    title = "Cumulative USDT printed and cumulative mining revenue"
    plt.title(title + " since 1/1/2017")
    axes[0,0].yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # format y axis with commas
    axes[0,0].xaxis.set_major_locator(mdates.WeekdayLocator())

    fig.text(0.85, 0.12, 'sellthedip.com', fontsize=10, color='dimgrey', ha='right', va='bottom', alpha=0.5)
    fig.text(0.25, 0.12, '@andr3w321', fontsize=10, color='dimgrey', ha='right', va='bottom', alpha=0.5)
    #plt.show()
    plt.savefig("./img/{}.jpg".format(title))

def graph_usdt_supply_vs_usdt_marketcap(df):
    df1 = df[df['Time'] >= '2017-01-01']
    df1 = df1[df1['Time'] <= '2020-01-01']
    df1["USDT_marketcap_custom"] = df1["USDT_supply"] * df1["coinbase/bitfinex"]
    df1 = df1[["Time","USDT_supply","USDT_marketcap","USDT_marketcap_custom"]]
    df1.columns = ["Time","coingecko USDT_supply","coingecko USDT_marketcap","true_USDT_marketcap (USDT_suppy*Coinbase BTC/Bitfinex BTC)"]
    df1 = df1.set_index("Time")
    fig, axes = plt.subplots(nrows=1, ncols=1, squeeze=False, figsize=(12,8))
    df1.plot(ax=axes[0,0])

    plt.xlabel("Date")
    plt.ylabel("Dollars")
    axes[0,0].yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # format y axis with commas

    title = "true_USDT_marketcap vs coingecko USDT_marketcap"
    plt.title(title)
    fig.text(0.85, 0.15, '@andr3w321', fontsize=10, color='gray', ha='right', va='bottom', alpha=0.5)
    #plt.show()
    plt.savefig("./img/{}.jpg".format(title))

def graph_usdt_supply_over_time(df):
    df1 = df[df['Time'] >= '2017-01-01']
    df1 = df1[["Time","USDT_supply"]]
    df1 = df1.set_index("Time")
    fig, axes = plt.subplots(nrows=1, ncols=1, squeeze=False, figsize=(12,8))
    df1.plot(ax=axes[0,0])

    plt.xlabel("Date")
    plt.ylabel("Dollars")
    axes[0,0].yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # format y axis with commas

    title = "USDT Supply Over Time"
    plt.title(title + "\nsource: coingecko.com")
    fig.text(0.85, 0.12, 'sellthedip.com', fontsize=10, color='dimgrey', ha='right', va='bottom', alpha=0.5)
    fig.text(0.25, 0.12, '@andr3w321', fontsize=10, color='dimgrey', ha='right', va='bottom', alpha=0.5)
    #plt.show()
    plt.savefig("./img/{}.jpg".format(title))

def graph_bitcoin_flows(df, n):
    df1 = df[df['Time'] >= '2020-12-01'].copy()
    new_col = "Bitcoin flows"
    df1[new_col] = df["last_{}_days_USDT_supply_increase".format(n)] - df1["{}_day_MinerRevenue".format(n)]

    df1 = df1[["Time",new_col,"bitstamp"]]
    df1 = df1.set_index("Time")
    fig, axes = plt.subplots(nrows=1, ncols=1, squeeze=False, figsize=(16,8))

    axes[0,0].bar(df1.index, df1[new_col], width=1)
    plt.xlabel("Date")
    plt.ylabel("Last {} Day Bitcoin Flows".format(n))
    title = "Last {} Day Bitcoin Flows and Bitcoin Price Over Time".format(n)
    plt.title(title)
    axes[0,0].yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # format y axis with commas

    # BTC price
    ax2 = axes[0,0].twinx()
    ax2.plot(df1.index, df1["bitstamp"], color='orange')
    ax2.set_ylabel("Bitstamp BTC Price")
    ax2.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # format y axis with commas
    axes[0,0].xaxis.set_major_locator(mdates.WeekdayLocator())

    fig.text(0.85, 0.12, 'sellthedip.com', fontsize=10, color='dimgrey', ha='right', va='bottom', alpha=0.5)
    fig.text(0.25, 0.12, '@andr3w321', fontsize=10, color='dimgrey', ha='right', va='bottom', alpha=0.5)
    #plt.show()
    plt.savefig("./img/{}.jpg".format(title))

def graph_miner_revenue_over_time(df, n, since_date):
    df1 = df[df['Time'] >= since_date].copy()
    new_col = "Miner Revenue"
    df1[new_col] = df1["MinerRevenue"] * -1.0
    df1 = df1[["Time",new_col,"bitstamp"]]
    df1 = df1.set_index("Time")
    fig, axes = plt.subplots(nrows=1, ncols=1, squeeze=False, figsize=(16,8))

    axes[0,0].bar(df1.index, df1[new_col], width=1)
    plt.xlabel("Date")
    plt.ylabel("Daily Miner Revenue")
    title = "Daily Miner Revenue and Bitcoin Price Over Time"
    plt.title(title + "\nsource: blockchain.info")
    axes[0,0].yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # format y axis with commas

    # BTC price
    ax2 = axes[0,0].twinx()
    ax2.plot(df1.index, df1["bitstamp"], color='orange')
    ax2.set_ylabel("Bitstamp BTC Price")
    ax2.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # format y axis with commas
    #axes[0,0].xaxis.set_major_locator(mdates.YearLocator())
    axes[0,0].xaxis.set_major_locator(mdates.WeekdayLocator())

    fig.text(0.85, 0.12, 'sellthedip.com', fontsize=10, color='dimgrey', ha='right', va='bottom', alpha=0.5)
    fig.text(0.25, 0.12, '@andr3w321', fontsize=10, color='dimgrey', ha='right', va='bottom', alpha=0.5)
    #plt.show()
    plt.savefig("./img/{}.jpg".format(title))

def graph_usdt_supply_change_over_time(df, n, since_date, include_btc_price=False, include_bfx_premium=False):
    df1 = df[df['Time'] >= since_date].copy()
    new_col = "Change in USDT supply over last {} days".format(n)
    df1[new_col] = df1["USDT_supply"] - df1["USDT_supply"].shift(n)
    fig, axes = plt.subplots(nrows=1, ncols=1, squeeze=False, figsize=(16,8))
    title = new_col
    df1["Time"] = pd.to_datetime(df1["Time"])
    df1 = df1.set_index("Time")
    if include_btc_price:
        df1 = df1[[new_col,"bitstamp"]]
        ax2 = axes[0,0].twinx()
        #df1["bitstamp"].plot(ax=ax2, color='blue')
        ax2.plot(df1.index, df1["bitstamp"], color='orange')
        title += " and Bitcoin price"

        ax2.set_ylabel("Bitstamp BTC Price")
        ax2.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # format y axis with commas
    elif include_bfx_premium:
        df1 = df1[[new_col,"coinbase/bitfinex","coinbase"]]
        ax2 = axes[0,0].twinx()
        ax2.plot(df1.index, df1["coinbase/bitfinex"], color='orange')
        title += " and USDT price"
        ax2.set_ylabel("USDT price (CoinbaseBTC/BitfinexBTC)")
        ax2.set_ylim([0.8, 1.2])
        axes[0,0].set_ylim([-2_000_000_000, 2_000_000_000])
    else:
        df1 = df1[[new_col]]

    axes[0,0].bar(df1.index, df1[new_col], width=1)
    #axes[0,0].tick_params(rotation=90)

    # set ticks only every year
    #axes[0,0].xaxis.set_major_locator(mdates.YearLocator())
    axes[0,0].xaxis.set_major_locator(mdates.WeekdayLocator())

    plt.xlabel("Date")
    axes[0,0].set_ylabel("USDT Supply Change in Dollars")
    axes[0,0].yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # format y axis with commas

    plt.title(title)
    fig.text(0.85, 0.12, 'sellthedip.com', fontsize=10, color='dimgrey', ha='right', va='bottom', alpha=0.5)
    fig.text(0.25, 0.12, '@andr3w321', fontsize=10, color='dimgrey', ha='right', va='bottom', alpha=0.5)
    #plt.show()
    plt.savefig("./img/{}.jpg".format(title))

def graph_usdt_price_vs_bitfinex_premium(df):
    df1 = df[df['Time'] >= '2017-01-01']
    df1 = df1[["Time","USDT_price","coinbase/bitfinex","coinbase/binance"]]
    ax = df1.set_index("Time").plot()

    plt.xlabel("Date")
    plt.ylabel("Dollars")
    plt.title("USDT_price vs coinbase/bitfinex price")
    #ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=4))
    plt.show()

def graph_premiums(df, data_source, exchanges, comparing_exchange):
    df1 = df[df['Time'] >= '2017-01-01'].copy()
    exchanges.remove(comparing_exchange)
    """
    #remove_exchanges = ["mtgox","cex.io","exmo","bit-x","bitfinex"]
    remove_exchanges = ["mtgox","bitstamp","coinbase","kraken","gemini","bit-x"]
    for exchange in remove_exchanges:
        if exchange in exchanges:
            exchanges.remove(exchange)
    #exchanges = ["bit-x"]
    #title_lead = "Bit-x"
    # if exchanges[0].startswith("cdd_"):
        # exchanges.remove("cdd_itbit")
    """
    #title_lead = "USDT exchanges."
    #exchanges = ["cdd_bitfinex","cdd_binance","cdd_poloniex"]
    #exchanges = ["cdd_bitstamp","cdd_kraken"]
    #title_lead = "USD exchanges."
    # exchanges = ["cdd_bittrex"]
    # title_lead = "Bittrex"
    exchanges = ["bitfinex"]
    title_lead = "coingecko USDT price vs Bitfinex"
    df1["Time"] = df1["Time"].str.replace(" 00:00:00","")
    col_names = []
    for exchange in exchanges:
        col_names.append("{}/{}".format(comparing_exchange, exchange))
        df1[col_names[-1]] = df1[comparing_exchange] / df1[exchange]
    col_names.append("USDT_price")
    df1 = df1[["Time"] + col_names]
    df1.columns = ["Time","coinbase/bitfinex","coingecko USDT_price"]
    df1 = df1.set_index("Time")
    fig, axes = plt.subplots(nrows=1, ncols=1, squeeze=False, figsize=(12,8))
    df1.plot(ax=axes[0,0])
    plt.xlabel("Date")
    plt.ylabel("Exchange premium to {}".format(comparing_exchange))
    title = "{} BTC price premium vs {} over time\nsource: {}".format(title_lead, comparing_exchange, data_source)
    plt.title(title)
    fig.text(0.85, 0.15, '@andr3w321', fontsize=10, color='gray', ha='right', va='bottom', alpha=0.5)
    #plt.show()
    plt.savefig("./img/{}.jpg".format(title.split('\n')[0]))

def save_bitcoinity_btc_exchange_correlation(df):
    #df1 = df[df['Time'] >= '2017-08-17']
    #df1 = df[df['Time'] >= '2019-01-01']
    #df1 = df[df['Time'] >= '2018-03-01']
    df1 = df[["Time","bitfinex","bitstamp","coinbase","kraken","mtgox","bit-x","cex.io","exmo","itbit","cdd_binance"]]
    df1.corr(method='pearson').to_csv("./data/bitcoinity-correlation-matrix.csv")

def save_usdt_supply_correlation(df):
    df1 = df[df['Time'] >= '2018-01-01']
    trial_days = [1,7,14,21,30,45,60,180]
    """
    for trial_day in trial_days:
        df_merged = add_forward_column(df_merged, "coinbase", trial_day)
        df_merged = add_trailing_column(df_merged, "USDT_supply", trial_day)
    """
    column_names = ["Time"]
    row_names = []
    col_names = []
    for trial_day in trial_days:
        row_names.append("last_{}_days_USDT_supply_increase".format(trial_day))
        col_names.append("forward_{}_day_bitstamp_return".format(trial_day))
    df2 = pd.DataFrame(index=row_names, columns=col_names)
    for row_name in row_names:
        for col_name in col_names:
            df2.loc[row_name][col_name] = df1[row_name].corr(df1[col_name], method='pearson')
    #df2 = df1.corr(method='pearson')
    df2.to_csv("./data/usdt-only-model-correlation-matrix.csv")

def graph_cdd_prices(timeframe):
    df = pd.read_csv("./data/cdd-combined-{}.csv".format(timeframe))
    del df["unix"]
    ax = df.set_index("Time").plot()
    plt.xlabel("Date")
    plt.ylabel("Dollars")
    plt.title("Cryptodatadownload.com BTC exchange prices over time")
    plt.show()

def graph_bitcoinity_prices(df):
    df1 = df[df['Time'] >= '2017-01-01'].copy()
    df1 = df1[["Time","coinbase"]]
    fig, axes = plt.subplots(nrows=1, ncols=1, squeeze=False, figsize=(16,8))
    df1 = df1.set_index("Time")
    df1.plot(ax=axes[0,0])
    plt.xlabel("Date")
    plt.ylabel("BTC Price")
    title = "Bitcoin price over time"
    plt.title(title)

    fig.text(0.85, 0.12, 'sellthedip.com', fontsize=10, color='dimgrey', ha='right', va='bottom', alpha=0.5)
    fig.text(0.25, 0.12, '@andr3w321', fontsize=10, color='dimgrey', ha='right', va='bottom', alpha=0.5)

    #plt.show()
    plt.savefig("./img/{}.jpg".format(title))

def save_cdd_btc_exchange_correlation(timeframe):
    df = pd.read_csv("./data/cdd-combined-{}.csv".format(timeframe))
    del df["unix"]
    df.corr(method='pearson').to_csv("./data/cdd-{}-correlation-matrix.csv".format(timeframe))

def get_readable_cdd_timeframe(timeframe):
    if timeframe == "d":
        return "day"
    elif timeframe == "1h":
        return "hour"
    elif timeframe == "minute":
        return "minute"

def graph_cdd_rolling_corr(timeframe, n):
    df = pd.read_csv("./data/cdd-combined-{}.csv".format(timeframe))
    non_bitstamp_exchanges = ["kraken","bitfinex","binance","poloniex","bittrex","itbit"]#,"gemini"]
    col_names = []
    for exchange in non_bitstamp_exchanges:
        col_name = "cdd_{}_{}_corr".format(exchange, n)
        col_names.append(col_name)
        df[col_name] = df["cdd_" + exchange].rolling(n).corr(df["cdd_bitstamp"])
    df = df[["Time"] + col_names]
    df.to_csv("tmp.csv")

    ax = df.set_index("Time").plot()
    plt.xlabel("Date")
    plt.ylabel("Correlation")
    plt.title("{} {} rolling correlation with bitstamp over time".format(n, get_readable_cdd_timeframe(timeframe)))
    plt.show()

def graph_bitcoinity_rolling_corr(n):
    df = pd.read_csv("./data/combined.csv")
    non_coinbase_exchanges = ["bitstamp","kraken","gemini","bitfinex","bit-x","cex.io","itbit"]#,"cdd_binance","exmo"]
    col_names = []
    for exchange in non_coinbase_exchanges:
        col_name = "{}_{}_corr".format(exchange, n)
        col_names.append(col_name)
        df[col_name] = df[exchange].rolling(n).corr(df["coinbase"])
    df = df[["Time"] + col_names]
    ax = df.set_index("Time").plot()
    plt.xlabel("Date")
    plt.ylabel("Correlation")
    plt.title("{} day rolling correlation with coinbase over time".format(n))
    plt.show()

def graph_usdt_supply_rolling_corr(df, n, window_size):
    df1 = df[df['Time'] >= '2018-01-01'].copy()
    df1["model"] = df1["last_{}_days_USDT_supply_increase".format(n)]# - df1["{}_day_MinerRevenue".format(n)]
    #df1["model"] = df1["model"] + 164000000
    df1 = df1[["Time","model","bitstamp"]]#,"forward_{}_day_bitstamp_return".format(n)]]
    #df1["{}_day_USDT_rolling_corr".format(window_size)] = df1["last_{}_days_USDT_supply_increase".format(n)].rolling(window_size).corr(df1["forward_{}_day_bitstamp_return".format(n)])
    df1 = df1.set_index("Time")
    #del df1["{}_day_USDT_rolling_corr".format(window_size)]
    fig, axes = plt.subplots(nrows=1, ncols=1, squeeze=False, figsize=(16,8))
    ax2 = axes[0,0].twinx()
    df1["bitstamp"].plot(ax=axes[0,0], color='orange')
    df1["model"].plot(ax=ax2, color='blue')
    axes[0,0].set_ylabel("Bitstamp")
    ax2.set_ylabel("model")
    #axes[0,0].set_ylim([-5000000000, 5000000000])
    #ax2.set_ylim([-0.8, 0.8])
    #axes[0,0].ticklabel_format(useOffset=False)
    #axes[0,0].ticklabel_format(style='plain', axis='y')

    axes[0,0].yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # format y axis with commas
    ax2.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # format y axis with commas

    plt.axhline(0, color='black') # draw black line at 0 on y-axis

    """
    df2.plot(ax=axes[1,0])
    plt.xlabel("Date")
    plt.ylabel("{} day USDT rolling correlation".format(n))
    #title = "{} BTC price premium vs {} over time\nsource: {}".format(title_lead, comparing_exchange, data_source)
    #plt.title(title)
    """

    # legend
    lines, labels = axes[0,0].get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc=0)

    fig.text(0.85, 0.15, '@andr3w321', fontsize=10, color='gray', ha='right', va='bottom', alpha=0.5)
    plt.show()
    #plt.savefig("./img/{}.jpg".format(title.split('\n')[0]))


def graph_daily_return_over_time(df, exchange):
    #df1 = df[df['Time'] >= '2013-06-01'].copy()
    df1 = df[["Time",exchange]]
    df1["daily_btc_return"] = df1[exchange] / df1[exchange].shift(1) -1
    df1 = df1.set_index("Time")
    fig, axes = plt.subplots(nrows=2, ncols=1, squeeze=False, figsize=(12,10))
    df1["daily_btc_return"].plot(ax=axes[0,0])
    axes[0,0].set_xlabel("Date")
    axes[0,0].set_ylabel("Daily BTC return")
    axes[0,0].set_title("Daily BTC return over time")

    df1[exchange].plot(ax=axes[1,0])
    axes[1,0].set_xlabel("Date")
    axes[1,0].set_ylabel("{} BTC price".format(exchange))
    axes[1,0].set_title("{} BTC price over time".format(exchange))
    plt.show()

def graph_daily_return_histogram(df, exchange):
    df1 = df[df['Time'] >= '2013-06-01'].copy()
    df1 = df1[["Time",exchange]]
    df1["daily_btc_return"] = df1[exchange] / df1[exchange].shift(1) -1
    data = df1["daily_btc_return"]
    plt.hist(data, bins = 40)
    plt.xlabel("Daily BTC return")
    plt.ylabel("Number of days since 2013-06-01 with this daily return")
    plt.title("Daily BTC returns distribution since 2013-06-01")
    plt.ylim([0, 40])
    plt.show()

def graph_usdc_vs_usdt(df):
    df1 = df[df['Time'] >= '2019-01-01'].copy()
    df1 = df1[["Time","USDC_marketcap","USDT_marketcap"]]
    ax = df1.set_index("Time").plot(figsize=(12,8))
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # format y axis with commas
    plt.xlabel("Date")
    plt.ylabel("Marketcap")
    title = "USDT vs USDC marketcap over time"
    plt.title(title)
    #plt.show()
    plt.savefig("./img/{}.jpg".format(title))

def graph_gtrends_vs_btc_price(df):
    df1 = df[df['Time'] >= '2013-01-01'].copy()
    df1 = df1[["Time","forward_14_day_bitstamp_return","google trends","bitstamp"]]
    df1 = df1.set_index("Time")
    df1 = df1.fillna(method='ffill', limit=8)
    fig, axes = plt.subplots(nrows=1, ncols=1, squeeze=False, figsize=(12,10))
    ax2 = axes[0,0].twinx()
    #df1["forward_14_day_bitstamp_return"].plot(ax=ax2, color='blue', label="forward 14 day bitstamp return")
    df1["bitstamp"].plot(ax=axes[0,0], color='blue', label="bitstamp BTC price")
    df1["google trends"].plot(ax=ax2, color='orange', label="'bitcoin' google trends")

    axes[0,0].yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # format y axis with commas
    axes[0,0].set_ylabel("Bitcoin Price")
    ax2.set_ylabel("'bitcoin' google trends")
    title = "Bitstamp bitcoin price vs 'bitcoin' google trends"
    plt.title(title)

    # legend
    lines, labels = axes[0,0].get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc=0)

    fig.text(0.85, 0.12, 'sellthedip.com', fontsize=10, color='dimgrey', ha='right', va='bottom', alpha=0.5)
    fig.text(0.25, 0.12, '@andr3w321', fontsize=10, color='dimgrey', ha='right', va='bottom', alpha=0.5)

    #plt.axhline(0, color='black') # draw black line at 0 on y-axis
    #df1["bitstamp"].plot(ax=axes[2,0], color='red')
    #ax = df2.set_index("date").plot(figsize=(12,8))

    #plt.show()
    plt.savefig("./img/{}.jpg".format(title))


df = pd.read_csv("./data/combined.csv")
df_cdd_d = pd.read_csv("./data/cdd-combined-d.csv")
del df_cdd_d["unix"]

### blog 1 - more accurate tether price
#graph_usdt_supply_vs_usdt_marketcap(df)
#graph_usdt_price_vs_bitfinex_premium(df)
#graph_premiums(df_cdd_d, "cryptodatadownload.com", get_cdd_exchanges(), "cdd_bitstamp")
#graph_premiums(df, "bitcoinity.org", get_bitcoinity_exchanges(), "coinbase")

#print_exchange_data_start_stop_dates(df, get_bitcoinity_exchanges())
#print_exchange_data_start_stop_dates(df_cdd_d, get_cdd_exchanges())

#save_bitcoinity_btc_exchange_correlation(df)
#save_cdd_btc_exchange_correlation("d")

#graph_cdd_prices("d")

#graph_cdd_rolling_corr("d", 30)
#graph_bitcoinity_rolling_corr(30)

### blog 2 - predicting btc price
#graph_gtrends_vs_btc_price(df)
#graph_usdt_supply_over_time(df, False)
graph_usdt_supply_change_over_time(df, 1, "2020-12-01", include_btc_price=True, include_bfx_premium=False)
# graph_usdt_supply_change_over_time(df, 1, True)
# graph_usdt_supply_change_over_time(df, 30, False)
# graph_usdt_supply_change_over_time(df, 30, True)
#graph_usdt_supply_change_over_time(df, 1, False, True)
#graph_bitcoinity_prices(df)
graph_miner_revenue_over_time(df,1, "2020-12-01")
#graph_usdt_supply_vs_miner_revenue(df)
# graph_bitcoin_flows(df, 1)
# graph_bitcoin_flows(df, 7)
# graph_bitcoin_flows(df, 30)

#save_usdt_supply_correlation(df)
#graph_usdt_supply_rolling_corr(df, 1, 1)

#graph_usdt_supply_vs_miner_revenue(df)

### random charts
#graph_daily_return_over_time(df, "bitstamp")
#graph_daily_return_histogram(df, "bitstamp")
#graph_usdc_vs_usdt(df)


# TODO graphs
# btc volume / usdt volume
# predicted btc return, actual btc return
# 20 day running correlation
# 30 day trailing tether prints
# 30 day trailing mining
