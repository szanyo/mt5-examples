# https://www.mql5.com/en/docs/python_metatrader5/mt5historydealstotal_py

from datetime import datetime
import MetaTrader5 as mt5

# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# get the number of deals in history
from_date = datetime(2020, 1, 1)
to_date = datetime.now()
deals = mt5.history_deals_total(from_date, to_date)
if deals > 0:
    print("Total deals=", deals)
else:
    print("Deals not found in history")

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()