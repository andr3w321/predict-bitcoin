import requests
import time
from pytrends.request import TrendReq
pytrend = TrendReq()

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

def download_btc_price_history():
    filename = DATA_DIR + "btc-price-history.csv"
    url = "http://data.bitcoinity.org/export_data.csv?c=e&currency=USD&data_type=price&t=l&timespan=all"
    download_file(url, filename)

def download_miners_revenue():
    filename = DATA_DIR + "miners-revenue.csv"
    url = "https://api.blockchain.info/charts/miners-revenue?timespan=all&format=csv"
    url = "https://api.blockchain.info/charts/miners-revenue?timespan=all&sampled=false&format=csv"
    download_file(url, filename)

def download_usdt_history():
    filename = DATA_DIR + "usdt.json"
    url = "https://api.coingecko.com/api/v3/coins/tether/market_chart/range?vs_currency=usd&from=1392577232&to={}".format(int(time.time()))
    download_file(url, filename)

def download_btc_history():
    filename = DATA_DIR + "btc.json"
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from=1392577232&to={}".format(int(time.time()))
    download_file(url, filename)

def download_gtrends():
    filename = DATA_DIR + "gtrends.csv"
    pytrend.build_payload(kw_list=['bitcoin'], timeframe='2011-01-01 2020-10-25')
    df = pytrend.interest_over_time()
    print(df)

    df.to_csv(filename)


download_btc_price_history()
download_miners_revenue()
download_usdt_history()
download_btc_history()
#download_gtrends()
