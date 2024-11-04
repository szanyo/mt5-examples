# https://www.mql5.com/en/docs/python_metatrader5/mt5ordercalcmargin_py

import MetaTrader5 as mt5

# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# get account currency
account_currency = mt5.account_info().currency
print("Account currency:", account_currency)

# arrange the symbol list
symbols = ("EURUSD", "GBPUSD", "USDJPY", "USDCHF", "EURJPY", "GBPJPY")
print("Symbols to check margin:", symbols)
action = mt5.ORDER_TYPE_BUY
lot = 0.1
for symbol in symbols:
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not found, skipped")
        continue
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol, True):
            print("symbol_select({}}) failed, skipped", symbol)
            continue
    ask = mt5.symbol_info_tick(symbol).ask
    margin = mt5.order_calc_margin(action, symbol, lot, ask)
    if margin != None:
        print("   {} buy {} lot margin: {} {}".format(symbol, lot, margin, account_currency));
    else:
        print("order_calc_margin failed: , error code =", mt5.last_error())

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()