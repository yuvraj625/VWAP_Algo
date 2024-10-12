import pandas as pd
import numpy as np

# Assuming you have a DataFrame 'df' with historical stock data containing columns: 'close', 'high', 'low', 'volume'
# Calculate VWAP using high, low, close, and volume columns
def calculate_vwap(df):
    df['tp'] = (df['high'] + df['low'] + df['close']) / 3
    df['vwap'] = (df['tp'] * df['volume']).cumsum() / df['volume'].cumsum()
    return df

# Function to identify crossover points for long and short positions
def generate_signals(df):
    df['long_condition'] = (df['close'] > df['vwap']) & (df['close'].shift(1) <= df['vwap'].shift(1))
    df['short_condition'] = (df['close'] < df['vwap']) & (df['close'].shift(1) >= df['vwap'].shift(1))
    return df

# Assuming a retracement percentage of 30%
retracement_percentage = 0.30

# Function to handle long and short position logic
def manage_positions(df):
    df['highest_since_entry'] = np.nan
    df['lowest_since_entry'] = np.nan

    # Iterate over rows to track the highest and lowest prices since entry
    for i in range(1, len(df)):
        if df.loc[i, 'long_condition']:
            df.loc[i, 'highest_since_entry'] = df.loc[i, 'close']
        elif df.loc[i - 1, 'highest_since_entry']:
            df.loc[i, 'highest_since_entry'] = max(df.loc[i - 1, 'highest_since_entry'], df.loc[i, 'high'])

        if df.loc[i, 'short_condition']:
            df.loc[i, 'lowest_since_entry'] = df.loc[i, 'close']
        elif df.loc[i - 1, 'lowest_since_entry']:
            df.loc[i, 'lowest_since_entry'] = min(df.loc[i - 1, 'lowest_since_entry'], df.loc[i, 'low'])

    return df

# Load your historical stock data into a DataFrame 'df' and call the functions
df = pd.read_csv('stock_data.csv')  # Placeholder for actual data
df = calculate_vwap(df)
df = generate_signals(df)
df = manage_positions(df)

print(df[['close', 'vwap', 'long_condition', 'short_condition', 'highest_since_entry', 'lowest_since_entry']])
