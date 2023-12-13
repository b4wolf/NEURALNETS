import numpy as np
import pandas as pd

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula 
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    km = 6367 * c
    return km

def find_nearest(df, lat, lon):
    """
    Find the nearest latitude and longitude in the dataframe to the given lat and lon
    """
    distances = df.apply(lambda row: haversine_distance(lat, lon, row['Latitude'], row['Longitude']), axis=1)
    min_distance_index = distances.idxmin()
    return df.loc[[min_distance_index]]

def split_csv_on_date_change(input_csv):
    """
    Splits a CSV file into multiple new CSV files each time the date format in 'Date Local' changes.

    Parameters:
    - input_csv (str): The path to the input CSV file.
    """
    df = pd.read_csv(input_csv)
    current_format = None
    start_index = 0

    for i, row in df.iterrows():
        date_local = row['Date Local']
        new_format = '-' in date_local

        if current_format is None:
            current_format = new_format
        elif current_format != new_format:
            # Date format changed, split and save the DataFrame up to the current row
            df_slice = df.iloc[start_index:i]
            output_file = f'split_{start_index}_{i-1}.csv'
            df_slice.to_csv(output_file, index=False)
            start_index = i
            current_format = new_format

    # Save the last slice
    if start_index < len(df):
        output_file = f'split_{start_index}_{len(df)-1}.csv'
        df.iloc[start_index:].to_csv(output_file, index=False)
def filter_wisconsin_rows(input_csv, output_csv):
    """
    Reads a CSV file, filters rows where 'State Name' is 'Wisconsin', and writes
    these rows to a new CSV file.

    Parameters:
    - input_csv (str): Path to the input CSV file.
    - output_csv (str): Path where the filtered CSV file will be saved.
    """
    chunk_size = 10000  # Adjust the chunk size based on your file's size and available memory
    first_chunk = True  # Flag to indicate if it's the first chunk

    for chunk in pd.read_csv(input_csv, chunksize=chunk_size):
        filtered_chunk = chunk[chunk['State Name'] == 'Wisconsin']
        
        if not filtered_chunk.empty:
            # Write header only for the first chunk and append for the others
            filtered_chunk.to_csv(output_csv, mode='a', header=first_chunk, index=False)
            first_chunk = False
def process(chunk):
    filtered_chunk = chunk[chunk['State Name'] == 'Wisconsin']

    if 'State Name' in filtered_chunk.columns:
        mean_value = filtered_chunk['DataColumn'].mean()
        print(f"Mean of 'DataColumn' for Wisconsin in this chunk: {mean_value}")
    else:
        print("Column 'DataColumn' not found in this chunk.")
