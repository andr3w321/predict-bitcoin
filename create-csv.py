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

def get_btc_df():
    df = pd.read_csv("./data/btc-price-history.csv")
    del df['bit-x']
    del df['cex.io']
    del df['exmo']
    del df['gemini']
    del df['itbit']
    del df['others']
    df["Time"] = df["Time"].str.replace(" UTC", "")
    return df

def get_miners_df():
    return pd.read_csv("./data/miners-revenue.csv", names=["Time","MinerRevenue"])

df_btc = get_btc_df()
df_miners = get_miners_df()
# merge df_btc and df_miners
df_merged = pd.merge(df_btc, df_miners, how="left", on=["Time"])
df_merged["Time"] = df_merged["Time"].str.replace(" 00:00:00","")

df_usdt = get_coingecko_df('./data/usdt.json', "USDT")
# merge df_usdt
df_merged = pd.merge(df_merged, df_usdt, how="left", on=["Time"])
# there's a few missing rows in USDT_marketcap and price, fill them with previous rows data
df_merged["USDT_marketcap"].fillna( method ='ffill', limit = 1, inplace = True) # limit = 1 means replace only 1 consecutive None row
df_merged["USDT_price"].fillna( method ='ffill', limit = 1, inplace = True) # limit = 1 means replace only 1 consecutive None row

df_cg_btc = get_coingecko_df('./data/btc.json', "BTC")
# merge df_cg_btc
df_merged = pd.merge(df_merged, df_cg_btc, how="left", on=["Time"])

# add bfx premium
df_merged["coinbase/bfx"] = df_merged["coinbase"] / df_merged["bitfinex"]
df_merged["bfx-coinbase"] = df_merged["bitfinex"] - df_merged["coinbase"]

df = df_merged
df["USDT_supply"] = df["USDT_marketcap"] / df["USDT_price"]

# 2 inputs, USDT prints, mining revenue, (Unknown FOMO FIAT)
# output, btc forward return
df = add_forward_column(df, "coinbase", 30)
df = add_trailing_column(df, "USDT_supply", 1)
df = add_trailing_column(df, "USDT_supply", 30)
#df["1_day_USDT_printing-MinerRevenue"] = df["last_1_days_USDT_supply_increase"] - df["MinerRevenue"]
df["30_day_MinerRevenue"] = df["MinerRevenue"].rolling(30, min_periods=30).sum()
# chart r and r^2
df.to_csv("./data/combined.csv", index=False)
