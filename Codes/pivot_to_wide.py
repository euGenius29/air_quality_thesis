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
print("DataFrame with new 'site_id' column:")
print(df[['site_name', 'site_id']].head())
print(df.head())

# Define the new columns to to pivot the DataFrame.
# Pivot for pm2.5_raw
pm2_5_wide = df.pivot_table(index='datetime',
                           columns='site_id',
                          values='pm2_5',
                          aggfunc=list)

# Pivot for pm2.5 calibrated
pm2_5_calibrated_wide = df.pivot_table(index='datetime',
                           columns='site_id',
                          values='pm2_5_calibrated_value',
                          aggfunc=list)

# Pivot for pm10_raw
pm10_wide = df.pivot_table(index='datetime',
                           columns='site_id',
                          values='pm10',
                          aggfunc=list)

# Pivot for pm10 calibrated
pm10_calibrated_wide = df.pivot_table(index='datetime',
                           columns='site_id',
                          values='pm10_calibrated_value',
                          aggfunc=list)
'''
# Combine all pivoted DataFrames into one.
frames = [pm2_5_wide, pm2_5_calibrated_wide, pm10_wide, pm10_calibrated_wide]
combined_wide_df = pd.concat(frames,
                             axis=1,
                             keys=['pm2_5_wide', 'pm2_5_calibrated_wide', 'pm10_wide', 'pm10_calibrated_wide'])

print("Pivoted DataFrame shape:", combined_wide_df.shape)
print("combined_wide_data head", combined_wide_df.head())
print("combined_wide_data columns", combined_wide_df.columns)
print("combined_wide_data tail", combined_wide_df.tail())
'''
# Combine all pivoted dataframes into one.
# Rename Columns and Concatenate

# Create a list of tuples with the DataFrame and a name for its columns.
frames_to_rename = [
    (pm2_5_wide, 'pm2_5_raw'),
    (pm2_5_calibrated_wide, 'pm2_5_calibrated'),
    (pm10_wide, 'pm10_raw'),
    (pm10_calibrated_wide, 'pm10_calibrated')
]

# Create a list to store the renamed DataFrames.
renamed_frames = []

# Loop through each DataFrame and rename its columns before adding it to the list.
for frame, name in frames_to_rename:
    # Use a dictionary comprehension to create new column names.
    rename_dict = {col: f"{name}_{col}" for col in frame.columns}
    renamed_frame = frame.rename(columns=rename_dict)
    renamed_frames.append(renamed_frame)

# Concatenate all the renamed DataFrames into a single, flat DataFrame.
combined_wide_df = pd.concat(renamed_frames, axis=1)
# Save the final wide-format DataFrame to a CSV file.
current_name = "02_wide_pm"
combined_wide_df.to_csv(fc.save_path(dm.csv_folder, current_name), index=True)

print("Final Combined DataFrame with Flattened Columns:")
print(combined_wide_df.head())
print("Final Combined DataFrame shape:", combined_wide_df.shape)