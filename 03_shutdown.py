# https://www.mql5.com/en/docs/python_metatrader5/mt5shutdown_py

import time

import MetaTrader5 as mt5

# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed")
    quit()

# display data on connection status, server name and trading account
print(mt5.terminal_info())
# display data on MetaTrader 5 version
print(mt5.version())

time.sleep(5)

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()