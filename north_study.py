import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_index = pd.read_csv("U:\\North\\index_data.csv")
df_index.trade_date = pd.to_datetime(df_index.trade_date)
df_index.set_index('trade_date', drop=True, inplace=True)
df_north_money = pd.read_csv("U:\\North\\north_data.csv")
df_north_money.trade_date = pd.to_datetime(df_north_money.trade_date)
df_north_money.set_index('trade_date', drop=True, inplace=True)

df_index_ret = df_index / df_index.shift(1) - 1
df_comb = df_index_ret.join(df_north_money['north_money'])
df_comb.dropna(inplace=True)

xin_north = df_comb[['xin9i', 'north_money']]

def cal_roll_corr(data, period=30):
    corrs = data.rolling(period).corr()
    corrs = corrs.dropna().iloc[1::2, 0]
    corrs = corrs.reset_index()
    corrs = corrs.set_index('trade_date')

    return corrs['xin9i']

cor = cal_roll_corr(xin_north, period=60)

def north_strategy(data, window, stdev_n, cost):

    df = data.copy().dropna()
    df['mid'] = df['north_money'].rolling(window).mean()
    stdev = df['north_money'].rolling(window).std()

    df['upper'] = df['mid'] + stdev_n * stdev
    df['lower'] = df['mid'] - stdev_n * stdev
    df['ret'] = df.close / df.close.shift(1) - 1
    df.dropna(inplace=True)

    df.loc[df['north_money'] > df.upper, 'signal'] = 1
    df.loc[df['north_money'] < df.lower, 'signal'] = -1
    df['position'] = df['signal'].shift(1)
    df['position'].fillna(method='ffill', inplace=True)
    df['position'].fillna(0, inplace=True)

    df.loc[df['position'] > df['position'].shift(1), 'capital_ret'] = \
        (df['position'] - df['position'].shift(1)) * (df.close / df.open - 1) * (1 - cost)
    df.loc[df['position'] < df['position'].shift(1), 'capital_ret'] = \
        (df['position'].shift(1) - df['position']) * (df.open / df.close.shift(1) - 1) * (1 - cost)
    df.loc[df['position'] == df['position'].shift(1), 'capital_ret'] = df['ret'] * df['position']
    df.capital_ret.fillna(0, inplace=True)

    df['net_value'] = (df.capital_ret + 1.0).cumprod()
    df['index_value'] = (df.ret + 1.0).cumprod()

    return df

df_xin_north = pd.read_excel("U:\\North\\xin_result.xlsx")
df_xin_north.trade_date = pd.to_datetime(df_xin_north.trade_date)
df_xin_north.set_index('trade_date', drop=True, inplace=True)

df_szse_north = pd.read_csv("U:\\North\\result_df.csv")
df_szse_north.trade_date = pd.to_datetime(df_szse_north.trade_date)
df_szse_north.set_index('trade_date', drop=True, inplace=True)

df_test = north_strategy(df_xin_north, 250, 1.5, 0.005)
df_szse_test = north_strategy(df_szse_north, 250, 1.5, 0.005)

print("asdf")
