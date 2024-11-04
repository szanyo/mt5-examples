# https://www.mql5.com/en/docs/python_metatrader5

from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
import MetaTrader5 as mt5

# connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

# request connection status and parameters
print(mt5.terminal_info())
# get data on MetaTrader 5 version
print(mt5.version())

# request 1000 ticks from EURAUD
euraud_ticks = mt5.copy_ticks_from("EURAUD",
                                   datetime(2024, 10, 28, 13),
                                   1000,
                                   mt5.COPY_TICKS_ALL)

print(f"Last error: {mt5.last_error()}")

# request ticks from AUDUSD within 2019.04.01 13:00 - 2019.04.02 13:00
audusd_ticks = mt5.copy_ticks_range("AUDUSD",
                                    datetime(2024, 10, 27, 13),
                                    datetime(2024, 10, 28, 13),
                                    mt5.COPY_TICKS_ALL)

print(f"Last error: {mt5.last_error()}")

# get bars from different symbols in a number of ways
eurusd_rates = mt5.copy_rates_from("EURUSD",
                                   mt5.TIMEFRAME_M1,
                                   datetime(2024, 10, 28, 13),
                                   1000)

print(f"Last error: {mt5.last_error()}")

eurgbp_rates = mt5.copy_rates_from_pos("EURGBP",
                                       mt5.TIMEFRAME_M1,
                                       0,
                                       1000)

print(f"Last error: {mt5.last_error()}")

eurcad_rates = mt5.copy_rates_range("EURCAD",
                                    mt5.TIMEFRAME_M1,
                                    datetime(2024, 10, 27, 13),
                                    datetime(2024, 10, 28, 13))

print(f"Last error: {mt5.last_error()}")

# shut down connection to MetaTrader 5
mt5.shutdown()

# DATA
print('euraud_ticks(', len(euraud_ticks), ')')
for val in euraud_ticks[:10]: print(val)

print('audusd_ticks(', len(audusd_ticks), ')')
for val in audusd_ticks[:10]: print(val)

print('eurusd_rates(', len(eurusd_rates), ')')
for val in eurusd_rates[:10]: print(val)

print('eurgbp_rates(', len(eurgbp_rates), ')')
for val in eurgbp_rates[:10]: print(val)

print('eurcad_rates(', len(eurcad_rates), ')')
for val in eurcad_rates[:10]: print(val)

# PLOT
# create DataFrame out of the obtained data
ticks_frame = pd.DataFrame(euraud_ticks)
# convert time in seconds into the datetime format
ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
# display ticks on the chart
plt.plot(ticks_frame['time'], ticks_frame['ask'], 'r-', label='ask')
plt.plot(ticks_frame['time'], ticks_frame['bid'], 'b-', label='bid')

# display the legends
plt.legend(loc='upper left')

# add the header
plt.title('EURAUD ticks')

# display the chart
plt.show()