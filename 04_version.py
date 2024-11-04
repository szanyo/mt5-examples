# https://www.mql5.com/en/docs/python_metatrader5/mt5version_py

import MetaTrader5 as mt5
import pandas as pd

# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# display data on MetaTrader 5 version
print(mt5.version())

# display data on connection status, server name and trading account 'as is'
print(mt5.terminal_info())
print()

# get properties in the form of a dictionary
terminal_info_dict = mt5.terminal_info()._asdict()
# convert the dictionary into DataFrame and print
df = pd.DataFrame(list(terminal_info_dict.items()), columns=['property', 'value'])
print("terminal_info() as dataframe:")
print(df[:-1])

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()