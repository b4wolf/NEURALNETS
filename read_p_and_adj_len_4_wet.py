import pandas as pd
from datetime import timedelta
df = pd.read_parquet('MKE.parquet')
df['valid'] = pd.to_datetime(df['valid'])
# Filter for the years 2020 and 2021
df_filtered = df[df['valid'].dt.year.isin([2020, 2020])]
df = pd.DataFrame(df_filtered)
df['valid'] = pd.to_datetime(df['valid']) + timedelta(minutes=8)
first_row = df.iloc[0].copy()
first_row['valid'] = first_row['valid'].replace(hour=0, minute=0, second=0, microsecond=0)
df = pd.concat([pd.DataFrame([first_row]), df]).reset_index(drop=True)
df = df[:-1]
df