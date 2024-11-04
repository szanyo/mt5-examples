# https://www.mql5.com/en/docs/python_metatrader5/mt5symbolselect_py

import MetaTrader5 as mt5
import pandas as pd

# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)
print()
# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# attempt to enable the display of the EURCAD in MarketWatch
selected = mt5.symbol_select("EURCAD", True)
if not selected:
    print("Failed to select EURCAD, error code =", mt5.last_error())
else:
    symbol_info = mt5.symbol_info("EURCAD")
    print(symbol_info)
    print("EURCAD: currency_base =", symbol_info.currency_base, "  currency_profit =", symbol_info.currency_profit,
          "  currency_margin =", symbol_info.currency_margin)
    print()

    # get symbol properties in the form of a dictionary
    print("Show symbol_info()._asdict():")
    symbol_info_dict = symbol_info._asdict()
    for prop in symbol_info_dict:
        print("  {}={}".format(prop, symbol_info_dict[prop]))
    print()

    # convert the dictionary into DataFrame and print
    df = pd.DataFrame(list(symbol_info_dict.items()), columns=['property', 'value'])
    print("symbol_info_dict() as dataframe:")
    print(df)

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()