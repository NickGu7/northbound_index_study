import pandas as pd
from datetime import datetime
from config import *

df_sse_north = pd.read_excel(sse_north_url, skiprows=4, usecols=['No.', 'SSE Stock Code', 'Stock Name'])
df_sse_north.columns = ['No.', 'Ticker', 'Description']
df_sse_north['Ticker'] = df_sse_north['Ticker'].map(lambda x: str(x)) + " CH Equity"
df_szse_north = pd.read_excel(szse_north_url, skiprows=4, usecols=['No.', 'SZSE Stock Code', 'Stock Name'])
df_szse_north.columns = ['No.', 'Ticker', 'Description']
df_szse_north['Ticker'] = df_szse_north['Ticker'].map(lambda x: str(x).zfill(6)) + " CH Equity"

df_sse_north['Notes'] = df_sse_north['No.'].map(lambda x: '' if type(x) == int else x)
df_szse_north['Notes'] = df_szse_north['No.'].map(lambda x: '' if type(x) == int else x)

df_north = df_sse_north.append(df_szse_north)[['Ticker', 'Description', 'Notes']].reset_index(drop=True)

df_south = pd.read_excel(south_url)
df_south.columns = ['Ticker', 'Chinese Name', 'Description']
df_south = df_south[['Ticker', 'Description']]
df_south['Ticker'] = df_south['Ticker'].map(lambda x: str(x) + ' HK Equity')

time_stamp = datetime.now()
writer = pd.ExcelWriter(eligi_path + "\\MMA Eligible List " + time_stamp.strftime("%Y%m%d") + ".xlsx")

df_north.to_excel(writer, index=False, sheet_name="Northbound")
df_south.to_excel(writer, index=False, sheet_name="Southbound")
writer.save()


