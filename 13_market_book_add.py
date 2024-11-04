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
added = mt5.market_book_add("EURUSD")
if not added:
    print("Failed to add EURUSD to MarketBook, error code =", mt5.last_error())
else:
    print("EURUSD added to MarketBook")
    print()

    # get the MarketBook for the EURUSD symbol
    book = mt5.market_book_get("EURUSD")
    if book is None:
        print("Failed to get MarketBook for EURUSD, error code =", mt5.last_error())
    else:
        print("MarketBook for EURUSD:")
        print(book)
        print()

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()