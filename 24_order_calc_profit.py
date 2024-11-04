# https://www.mql5.com/en/docs/python_metatrader5/mt5ordercalcprofit_py

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
symbols = ("EURUSD", "GBPUSD", "USDJPY")
print("Symbols to check margin:", symbols)
# estimate profit for buying and selling
lot = 1.0
distance = 300
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
    point = mt5.symbol_info(symbol).point
    symbol_tick = mt5.symbol_info_tick(symbol)
    ask = symbol_tick.ask
    bid = symbol_tick.bid
    buy_profit = mt5.order_calc_profit(mt5.ORDER_TYPE_BUY, symbol, lot, ask, ask + distance * point)
    if buy_profit != None:
        print("   buy {} {} lot: profit on {} points => {} {}".format(symbol, lot, distance, buy_profit,
                                                                      account_currency));
    else:
        print("order_calc_profit(ORDER_TYPE_BUY) failed, error code =", mt5.last_error())
    sell_profit = mt5.order_calc_profit(mt5.ORDER_TYPE_SELL, symbol, lot, bid, bid - distance * point)
    if sell_profit != None:
        print("   sell {} {} lots: profit on {} points => {} {}".format(symbol, lot, distance, sell_profit,
                                                                        account_currency));
    else:
        print("order_calc_profit(ORDER_TYPE_SELL) failed, error code =", mt5.last_error())
    print()

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()