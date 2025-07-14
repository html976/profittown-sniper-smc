import pandas as pd

def load_data(filepath: str) -> pd.DataFrame:
    """Loads historical price data from a CSV file."""
    df = pd.read_csv(filepath)
    # Ensure columns are named correctly
    df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
    # Convert time to datetime and set as index
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    print(f"Loaded {len(df)} rows of data.")
    return df
