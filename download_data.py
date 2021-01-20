import requests
import time
from pytrends.request import TrendReq
pytrend = TrendReq()
import datetime
import pytrends_weekly as pyt

DATA_DIR = "./data/"

def download_file(url, filename):
    """ Download large file in chunks."""
    with requests.get(url, stream=True) as res:
        if res.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in res.iter_content(chunk_size=8192): 
                    f.write(chunk)
        else:
            raise ValueError("{} {}".format(res.status_code, url))
    return filename

def download_bitcoinity_btc_price_history():
    filename = DATA_DIR + "bitcoinity-btc-price-history.csv"
    url = "http://data.bitcoinity.org/export_data.csv?c=e&currency=USD&data_type=price&t=l&timespan=all"
    download_file(url, filename)

def download_miners_revenue():
    filename = DATA_DIR + "miners-revenue.csv"
    url = "https://api.blockchain.info/charts/miners-revenue?timespan=all&format=csv"
    url = "https://api.blockchain.info/charts/miners-revenue?timespan=all&sampled=false&format=csv"
    download_file(url, filename)

def download_coingecko_usdt_history():
    filename = DATA_DIR + "coingecko-usdt.json"
    url = "https://api.coingecko.com/api/v3/coins/tether/market_chart/range?vs_currency=usd&from=1392577232&to={}".format(int(time.time()))
    download_file(url, filename)

def download_coingecko_btc_history():
    filename = DATA_DIR + "coingecko-btc.json"
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from=1392577232&to={}".format(int(time.time()))
    download_file(url, filename)

def download_coingecko_usdc_history():
    filename = DATA_DIR + "coingecko-usdc.json"
    url = "https://api.coingecko.com/api/v3/coins/usd-coin/market_chart/range?vs_currency=usd&from=1392577232&to={}".format(int(time.time()))
    download_file(url, filename)


def download_gtrends():
    filename = DATA_DIR + "gtrends.csv"
    df = pyt.get_longterm_weekly(["bitcoin"], "2009-01-01 " + str(datetime.datetime.today()).split(' ')[0])
    df.to_csv(filename)

def download_cryptodatadownload(exchange, timeframe, symbol):
    if timeframe not in ["d","1h","minute"]:
        raise ValueError("Wrong timeframe input. Must be 'd','1h' or 'minute'")
    if exchange == "gemini" and timeframe == "d":
        url = "http://www.cryptodatadownload.com/cdd/{}_{}_{}.csv".format(exchange, symbol, "day")
    elif exchange == "gemini" and timeframe == "1h":
        url = "http://www.cryptodatadownload.com/cdd/{}_{}_{}.csv".format(exchange, symbol, "1hr")
    else:
        url = "http://www.cryptodatadownload.com/cdd/{}_{}_{}.csv".format(exchange, symbol, timeframe)
    filename = DATA_DIR + "cdd-{}-{}-{}.csv".format(exchange, symbol, timeframe)
    download_file(url, filename)

# mtgox price history source - https://bitcoincharts.com/charts/mtgoxUSD#tgSzm1g10zm2g25zv

download_bitcoinity_btc_price_history()
download_miners_revenue()
download_coingecko_usdt_history()
download_coingecko_btc_history()
download_coingecko_usdc_history()
download_gtrends()

# download_cryptodatadownload("Bitstamp","d","BTCUSD")
# download_cryptodatadownload("Binance","d","BTCUSDT")
# download_cryptodatadownload("Bitfinex","d","BTCUSD")
# download_cryptodatadownload("Kraken","d","BTCUSD")
# download_cryptodatadownload("gemini","d","BTCUSD")
# download_cryptodatadownload("Bittrex","d","BTCUSD")
# download_cryptodatadownload("Poloniex","d","BTCUSDT")
# download_cryptodatadownload("Itbit","d","BTCUSD")

# download_cryptodatadownload("Bitstamp","1h","BTCUSD")
# download_cryptodatadownload("Binance","1h","BTCUSDT")
# download_cryptodatadownload("Bitfinex","1h","BTCUSD")
# download_cryptodatadownload("Kraken","1h","BTCUSD")
# download_cryptodatadownload("gemini","1h","BTCUSD")

# download_cryptodatadownload("Bitstamp","minute","BTCUSD")
# download_cryptodatadownload("Binance","minute","BTCUSDT")
# download_cryptodatadownload("Bitfinex","minute","BTCUSD")
# download_cryptodatadownload("Kraken","minute","BTCUSD")

