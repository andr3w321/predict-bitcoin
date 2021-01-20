from pytrends.request import TrendReq
from dateutil import parser
import datetime
import pandas as pd
pytrend = TrendReq()

def combine(kw_list, df1, start, end):
    # get five years data from 9 years ago to 4 years ago
    endless9 = end - datetime.timedelta(days=365.25*9)
    endless4 = endless9 + datetime.timedelta(days=365.25*5)
    if endless9 < start:
        endless9 = start
    pytrend.build_payload(kw_list=kw_list, timeframe=endless9.strftime("%Y-%m-%d") + " " + endless4.strftime("%Y-%m-%d"))
    df2 = pytrend.interest_over_time()
    # find an overlapping factor
    factor = (df1[kw_list] / df2[kw_list]).mean()
    df2[kw_list] = df2[kw_list] * factor
    df1[kw_list] = df1[kw_list].astype(float) # avoid merging int and float column warning
    # merge the dataframes
    df_merged = pd.merge(df1, df2, on=(df1.columns & df2.columns).tolist(), how='outer', left_index=True, right_index=True)
    if endless9 != start:
        return combine(kw_list, df_merged, start, df2.index[-1])
    else:
        return df_merged

def get_longterm_weekly(kw_list, timeframe):
    # first get raw request
    pytrend.build_payload(kw_list=kw_list, timeframe=timeframe)
    df = pytrend.interest_over_time()
    delta = df.index[-1] - df.index[0]
    five_years = datetime.timedelta(days=365.25*5)
    if delta < five_years:
        return df
    else:
        # parse timeframe string into datetime objects
        start_str, end_str = timeframe.split(" ")
        start = parser.parse(start_str)
        end = parser.parse(end_str)
        # get latest five year df
        endless5 = end - datetime.timedelta(days=365.25*5)
        pytrend.build_payload(kw_list=kw_list, timeframe=endless5.strftime("%Y-%m-%d") + " " + end.strftime("%Y-%m-%d"))
        latest_df = pytrend.interest_over_time()
        return combine(kw_list, latest_df, start, latest_df.index[-1])
