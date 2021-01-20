import pandas as pd
import json
import datetime

def add_trailing_column(df, old_column, diff):
    df["last_{0}_days_{1}_increase".format(diff, old_column)] = df[old_column] - df[old_column].shift(diff)
    return df

def add_forward_column(df, old_column, diff):
    df["forward_{0}_day_{1}_return".format(diff, old_column)] = df[old_column].shift(diff * -1) / df[old_column] - 1
    return df

def get_coingecko_df(filename, coin_name):
    with open(filename, 'r') as f:
        data = f.read()
    obj = json.loads(data)
    df = pd.DataFrame(obj['market_caps'], columns=['Time', "{0}_marketcap".format(coin_name)])
    df2 = pd.DataFrame(obj['prices'], columns=['Time', "{0}_price".format(coin_name)])
    df_merged = pd.merge(df, df2, how="left", on=["Time"])
    df_merged['Time'] = pd.to_datetime(df_merged['Time']/1000, unit='s')
    df_merged['Time'] = df_merged.apply(lambda x: str(x['Time']).split(' ')[0], axis=1) # convert timestamp to date
    return df_merged

def get_bitcoinity_btc_df():
    df = pd.read_csv("./data/bitcoinity-btc-price-history.csv")
    del df['others']
    df["Time"] = df["Time"].str.replace(" UTC", "")
    return df

def get_miners_df():
    return pd.read_csv("./data/miners-revenue.csv", names=["Time","MinerRevenue"])

def get_mtgox_df():
    df = pd.read_csv("./data/mtgox-btc-price-history.csv", usecols=["Timestamp","Close"])
    df.columns = ["Time","mtgox"]
    df["Time"] = df["Time"].str.replace(" 00:00:00","")
    return df

def get_cdd_df(exchange, symbol, timeframe, delete_columns=[]):
    df = pd.read_csv("./data/cdd-{}-{}-{}.csv".format(exchange, symbol, timeframe), skiprows=1)
    df.columns = map(str.lower, df.columns)
    if exchange in ["Bitstamp","Binance","Kraken","Bitfinex","Poloniex"]:
        df = df[["unix","date","open"]]
    elif exchange in ["gemini","Bittrex","Itbit"]:
        df = df[["unix timestamp","date","open"]]
    else:
        raise ValueError("Unknown exchange for get_cdd_df()")
    df.columns = ["unix","Time","cdd_{}".format(exchange.lower())]
    unix_year_2255 = 9000000000
    df['unix'] = df['unix'].apply(lambda x: x / 1000 if x > unix_year_2255 else x) # weird bug where bitfinex unix time changes number of digits after 2020-07-18
    for delete_column in delete_columns:
        del df[delete_column]
    return df

def combine_cdds(timeframe):
    df1 = get_cdd_df("Bitstamp", "BTCUSD", timeframe)
    df2 = get_cdd_df("Bitfinex", "BTCUSD", timeframe, ["Time"])
    df3 = get_cdd_df("Binance", "BTCUSDT", timeframe, ["Time"])
    df4 = get_cdd_df("Kraken", "BTCUSD", timeframe, ["Time"])
    df_merged = pd.merge(df1, df2, how="left", on=["unix"]) 
    df_merged = pd.merge(df_merged, df3, how="left", on=["unix"])
    df_merged = pd.merge(df_merged, df4, how="left", on=["unix"])
    if timeframe in ["d"]:
        df5 = get_cdd_df("Bittrex", "BTCUSD", timeframe, ["Time"])
        df6 = get_cdd_df("Poloniex", "BTCUSDT", timeframe, ["Time"])
        df7 = get_cdd_df("Itbit", "BTCUSD", timeframe, ["Time"])
        df_merged = pd.merge(df_merged, df5, how="left", on=["unix"])
        df_merged = pd.merge(df_merged, df6, how="left", on=["unix"])
        df_merged = pd.merge(df_merged, df7, how="left", on=["unix"])
    if timeframe in ["d","1h"]:
        df99 = get_cdd_df("gemini", "BTCUSD", "1h", ["Time"])
        df_merged = pd.merge(df_merged, df99, how="left", on=["unix"])
    df_merged.sort_values(by="Time", ascending=True).to_csv("./data/cdd-combined-{}.csv".format(timeframe), index=False)

def get_googletrends_df():
    df = pd.read_csv("./data/gtrends.csv")
    df.columns = ["Time","google trends","google trends isPartial"]
    return df

df_bitcoinity_btc = get_bitcoinity_btc_df()
df_miners = get_miners_df()
# merge df_btc and df_miners
df_merged = pd.merge(df_bitcoinity_btc, df_miners, how="left", on=["Time"])
df_merged["Time"] = df_merged["Time"].str.replace(" 00:00:00","")

df_usdt = get_coingecko_df('./data/coingecko-usdt.json', "USDT")
# merge df_usdt
df_merged = pd.merge(df_merged, df_usdt, how="left", on=["Time"])
# there's a few missing rows in USDT_marketcap and price, fill them with previous rows data
df_merged["USDT_marketcap"].fillna( method ='ffill', limit = 1, inplace = True) # limit = 1 means replace only 1 consecutive None row
df_merged["USDT_price"].fillna( method ='ffill', limit = 1, inplace = True) # limit = 1 means replace only 1 consecutive None row

df_coingecko_btc = get_coingecko_df('./data/coingecko-btc.json', "BTC")
# merge df_coingecko_btc
df_merged = pd.merge(df_merged, df_coingecko_btc, how="left", on=["Time"])

df_coingecko_usdc = get_coingecko_df('./data/coingecko-usdc.json', "USDC")
# merge df_coingecko_btc
df_merged = pd.merge(df_merged, df_coingecko_usdc, how="left", on=["Time"])

#df = df_merged
df_merged["USDT_supply"] = df_merged["USDT_marketcap"] / df_merged["USDT_price"]

# 2 inputs, USDT prints, mining revenue, (Unknown FOMO FIAT)
# output, btc forward return
trial_days = [1,7,14,21,30,45,60,180,365]
for trial_day in trial_days:
    df_merged = add_forward_column(df_merged, "bitstamp", trial_day)
    df_merged = add_trailing_column(df_merged, "USDT_supply", trial_day)
    df_merged["{}_day_MinerRevenue".format(trial_day)] = df_merged["MinerRevenue"].rolling(trial_day, min_periods=trial_day).sum()

# mtgox
df_mtgox = get_mtgox_df()
df_merged = pd.merge(df_merged, df_mtgox, how="left", on=["Time"])

# binance # binance merge has an error, creates some double "Time" rows like 2020-11-20
#df_binance = get_cdd_df("Binance","BTCUSDT","d", ["unix"])
#df_binance["Time"] = df_binance["Time"].str.replace(" 00:00:00","")
#df_merged = pd.merge(df_merged, df_binance, how="left", on=["Time"])

# add bfx premium
df_merged["coinbase/bitfinex"] = df_merged["coinbase"] / df_merged["bitfinex"]
df_merged["bitfinex-coinbase"] = df_merged["bitfinex"] - df_merged["coinbase"]

# add binance premium
#df_merged["coinbase/binance"] = df_merged["coinbase"] / df_merged["cdd_binance"]

# add google trends data
df_googletrends = get_googletrends_df()
df_merged = pd.merge(df_merged, df_googletrends, how="left", on=["Time"])

# chart r and r^2
## save combined.csv and combined.js
df_merged.to_csv("./data/combined.csv", index=False)
df_merged.to_json("./data/combined.json")
# prepend "var data = " to json file so can be read as javascript data
with open('./data/combined.json', 'r') as original: data = original.read()
with open('./data/combined.js', 'w') as modified: modified.write("var combined = " + data)

combine_cdds("d")
combine_cdds("1h")
combine_cdds("minute")
