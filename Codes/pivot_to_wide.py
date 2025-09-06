"""
This module takes a long-format DataFrame and pivots it to a wide format based on specified columns.
"""
import re
import pandas as pd
import file_control as fc
import data_merging as dm


# Load the combined dataframe from the data_merging module.
df = dm.df.copy()

# Create a shorter site identifier based on site name.
site_id = "site_id"
df[site_id] = (
    df['site_name']             #site_id will be based on this column
    .str.split(",")             #split the long name using comma as delimiter
    .str[0]                     #take the first part of the split name
    .str.strip()                #remove leading/trailing whitespace
    .str.lower()                #convert the selected part of name to lowercase
    .str.replace(" ", "_")      #replace spaces with underscores
)

# Replace any missing device name with 'unknown_device'
df['device_name'] = df['device_name'].fillna('unknown_device')
print("DataFrame with new 'site_id' column:")
print(df[['site_name', 'site_id', 'device_name']].head())
print(df.head)

# Define the new columns to to pivot the DataFrame.
# Pivot for pm2.5_raw
pm2_5_wide = df.pivot_table(index='datetime',
                           columns=['site_id', 'device_name'],
                          values='pm2_5',
                          aggfunc=list)

# Pivot for pm2.5 calibrated
pm2_5_calibrated_wide = df.pivot_table(index='datetime',
                           columns=['site_id', 'device_name'],
                          values='pm2_5_calibrated_value',
                          aggfunc=list)

# Pivot for pm10_raw
pm10_wide = df.pivot_table(index='datetime',
                           columns=['site_id', 'device_name'],
                          values='pm10',
                          aggfunc=list)

# Pivot for pm10 calibrated
pm10_calibrated_wide = df.pivot_table(index='datetime',
                           columns=['site_id', 'device_name'],
                          values='pm10_calibrated_value',
                          aggfunc=list)

# Combine all pivoted DataFrames into one.
frames = [pm2_5_wide, pm2_5_calibrated_wide, pm10_wide, pm10_calibrated_wide]
combined_wide_df = pd.concat(frames,
                             axis=1,
                             keys=['pm2_5_wide', 'pm2_5_calibrated_wide', 'pm10_wide', 'pm10_calibrated_wide'])

print("Pivoted DataFrame shape:", combined_wide_df.shape)
print(combined_wide_df.head())
