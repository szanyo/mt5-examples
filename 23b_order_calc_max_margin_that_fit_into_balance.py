import MetaTrader5 as mt5

# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Retrieve account information
account_info = mt5.account_info()
if account_info is None:
    print("Cannot get account info, error code =", mt5.last_error())
    mt5.shutdown()
    quit()

# Account balance and currency
balance = account_info.balance
account_currency = account_info.currency
print("Account Balance:", balance, account_currency)

# Arrange the symbol list
symbols = ("EURUSD", "GBPUSD", "USDJPY", "USDCHF", "EURJPY", "GBPJPY")

# Calculate max lot size for each symbol based on minimum lot margin for both BUY and SELL
for symbol in symbols:
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not found, skipped")
        continue
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol, True):
            print(f"symbol_select({symbol}) failed, skipped")
            continue

    min_lot = symbol_info.volume_min  # Minimum lot size for this symbol
    tick_info = mt5.symbol_info_tick(symbol)

    # Check that we have valid tick info (ask and bid prices)
    if tick_info is None:
        print(f"Failed to get tick info for {symbol}, skipped")
        continue

    # Calculate for BUY order
    ask = tick_info.ask
    margin_min_lot_buy = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, symbol, min_lot, ask)
    if margin_min_lot_buy is None:
        print(f"order_calc_margin failed for BUY {symbol}, error code =", mt5.last_error())
    else:
        max_lot_buy = (balance // margin_min_lot_buy) * min_lot
        actual_margin_buy = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, symbol, max_lot_buy, ask)

        # Validation for BUY
        next_lot_buy = max_lot_buy + min_lot
        next_margin_buy = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, symbol, next_lot_buy, ask)
        if actual_margin_buy <= balance and (next_margin_buy is None or next_margin_buy > balance):
            print(f"Validation passed for BUY {symbol}: Maximum lot size {max_lot_buy} fits within balance {balance}")
        else:
            print(
                f"Validation failed for BUY {symbol}: Calculated max lot size may exceed balance or boundary check failed")

        print(
            f"BUY - Maximum lot size for {symbol} at ask price {ask} is {max_lot_buy} lots, requiring {actual_margin_buy} {account_currency}"
        )

    # Calculate for SELL order
    bid = tick_info.bid
    margin_min_lot_sell = mt5.order_calc_margin(mt5.ORDER_TYPE_SELL, symbol, min_lot, bid)
    if margin_min_lot_sell is None:
        print(f"order_calc_margin failed for SELL {symbol}, error code =", mt5.last_error())
    else:
        max_lot_sell = (balance // margin_min_lot_sell) * min_lot
        actual_margin_sell = mt5.order_calc_margin(mt5.ORDER_TYPE_SELL, symbol, max_lot_sell, bid)

        # Validation for SELL
        next_lot_sell = max_lot_sell + min_lot
        next_margin_sell = mt5.order_calc_margin(mt5.ORDER_TYPE_SELL, symbol, next_lot_sell, bid)
        if actual_margin_sell <= balance and (next_margin_sell is None or next_margin_sell > balance):
            print(f"Validation passed for SELL {symbol}: Maximum lot size {max_lot_sell} fits within balance {balance}")
        else:
            print(
                f"Validation failed for SELL {symbol}: Calculated max lot size may exceed balance or boundary check failed")

        print(
            f"SELL - Maximum lot size for {symbol} at bid price {bid} is {max_lot_sell} lots, requiring {actual_margin_sell} {account_currency}"
        )

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
