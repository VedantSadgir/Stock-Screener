import pandas as pd
from nsetools import Nse
import talib

# Define the stock symbol and time period
symbol = 'DLF'
start_date = '2023-06-14'
end_date = '2023-06-14'

# Instantiate the Nse object
nse = Nse()

# Get the historical data for the stock
data = nse.get_history(symbol, index=True, start=start_date, end=end_date)

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(data)

# Calculate RSI and Stochastic RSI using the talib library
rsi = talib.RSI(df['Close'])
stoch_rsi = talib.STOCHRSI(df['Close'])

# Define a variable to track whether we're currently in a position or not
in_position = False

# Iterate over the data and implement the strategy
for i in range(1, len(df)):
    # Check if RSI and Stochastic RSI are both above 50
    if rsi[i] > 50 and stoch_rsi[i] > 50:
        if in_position:
            # Sell the stock if currently in a position and volume exceeds previous candle volume
            if df['Volume'].iloc[i] > df['Volume'].iloc[i-1]:
                print('Sell', symbol, 'at ₹', df['Close'].iloc[i], '- Volume exceeded previous candle volume')
                in_position = False
    else:
        if not in_position:
            # Buy the stock if not already in a position
            in_position = True

# Check if still in position at the end of the data
if in_position:
    print('Still in position for', symbol, '- Last close price: ₹', df['Close'].iloc[-1])
