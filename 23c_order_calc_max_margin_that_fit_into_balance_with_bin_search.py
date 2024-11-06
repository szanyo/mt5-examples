import MetaTrader5 as mt5

# MetaTrader 5 inicializálása
if not mt5.initialize():
    print("Az inicializálás nem sikerült, hiba:", mt5.last_error())
    quit()

# Számlainformációk lekérése
account_info = mt5.account_info()
if account_info is None:
    print("Nem sikerült lekérni a számlainformációkat, hiba:", mt5.last_error())
    mt5.shutdown()
    quit()

balance = account_info.balance
account_currency = account_info.currency
print("Egyenleg:", balance, account_currency)

# Szimbólumok és műveletek definiálása
symbols = ("EURUSD", "GBPUSD", "USDJPY", "USDCHF", "EURJPY", "GBPJPY")
order_types = {"BUY": mt5.ORDER_TYPE_BUY, "SELL": mt5.ORDER_TYPE_SELL}

# Maximum lot kiszámítása mind BUY, mind SELL esetén bináris kereséssel
for symbol in symbols:
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None or not symbol_info.visible:
        print(f"{symbol} nem található vagy nem látható, kihagyva.")
        continue

    min_lot = symbol_info.volume_min  # Minimum lot méret
    max_lot_increment = min_lot  # Lépés a lot méret növeléséhez

    for order_name, order_type in order_types.items():
        price = mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid

        # Minimum margin kiszámítása a minimum lot mérethez
        sub_request = {"action": order_type, "volume": min_lot, "price": price}
        min_margin_lot = mt5.order_calc_margin(order_type, symbol, min_lot, price)
        if min_margin_lot is None:
            print(f"{symbol} {order_name} - Nem sikerült lekérni a minimális margin értéket.")
            continue

        # Bináris keresés kezdőértékei
        low = min_lot
        high = (balance // min_margin_lot) * min_lot  # Felső becslés a max lot méretre
        max_lot = low

        # Bináris keresés ciklus
        while low <= high:
            mid_lot = (low + high) / 2  # Középső érték a lot méret tartományában
            sub_request["volume"] = mid_lot
            mid_margin = mt5.order_calc_margin(order_type, symbol, mid_lot, price)

            if mid_margin is None:
                print(f"{symbol} {order_name} - Hiba a margin számítás során a lot méret {mid_lot} esetén.")
                break

            if mid_margin <= balance:
                max_lot = mid_lot  # Frissítjük a max lot méretet, ha még belefér az egyenlegbe
                low = mid_lot + min_lot  # Felsőbb tartományra keresünk
            else:
                high = mid_lot - min_lot  # Alsóbb tartományra keresünk

        # Végső validáció a maximális lot mérethez
        print(f"{order_name} - Maximum lot méret {symbol} számára: {max_lot} lot, amihez szükséges margin: {mid_margin} {account_currency}")

# MetaTrader 5 kapcsolat lezárása
mt5.shutdown()
