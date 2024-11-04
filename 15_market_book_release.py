# https://www.mql5.com/en/docs/python_metatrader5/mt5marketbookadd_py

import MetaTrader5 as mt5

# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)
print()
# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# attempt to add the EURUSD symbol to MarketBook
removed = mt5.market_book_release("EURUSD")
if not removed:
    print("Failed to release EURUSD from MarketBook, error code =", mt5.last_error())

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()