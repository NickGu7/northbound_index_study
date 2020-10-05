import requests
from bs4 import BeautifulSoup
import pandas as pd
from config import *

r_sse_north_hold = requests.get(sse_north_hold_url)
soup_sse_north_hold = BeautifulSoup(r_sse_north_hold.content, "html.parser")

sse_stock_list_raw = [x.find('div', class_='mobile-list-body').text
                      for x in soup_sse_north_hold.find_all('td', class_='col-stock-code')]



print("a")