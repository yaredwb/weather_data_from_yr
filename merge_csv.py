import pandas as pd

# Specify the exact files we want to merge
files = [
    'Øygarden_temperature_2015-01-01_to_2015-12-31.csv',
    'Øygarden_temperature_2016-01-01_to_2016-12-31.csv',
    'Øygarden_temperature_2017-01-01_to_2017-12-31.csv',
    'Øygarden_temperature_2018-01-01_to_2018-12-31.csv',
    'Øygarden_temperature_2019-01-01_to_2019-12-31.csv',
    'Øygarden_temperature_2020-01-01_to_2020-12-31.csv',
    'Øygarden_temperature_2021-01-01_to_2021-12-31.csv',
    'Øygarden_temperature_2022-01-01_to_2022-12-31.csv',
    'Øygarden_temperature_2023-01-01_to_2023-12-31.csv',
    'Øygarden_temperature_2024-01-01_to_2025-01-31.csv'
]

# Initialize an empty list to store dataframes
dfs = []

# Read each CSV file and append to list
for file in files:
    try:
        df = pd.read_csv(file)
        dfs.append(df)
    except FileNotFoundError:
        print(f"Warning: File {file} not found")

# Concatenate all dataframes
merged_df = pd.concat(dfs, ignore_index=True)

# Sort by date
merged_df = merged_df.sort_values('date')

# Remove any duplicates
merged_df = merged_df.drop_duplicates()

# Replace dates with sequential numbers starting from 1
merged_df['date'] = range(1, len(merged_df) + 1)

# Save to new CSV file with comma as decimal separator and semicolon as delimiter
merged_df.to_csv('Øygarden_temperature_2015_2025.csv', 
                index=False, 
                sep=';',
                decimal=',')
print("Merge complete!")
