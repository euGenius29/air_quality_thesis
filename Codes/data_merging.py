"""
This module combines multiple CSV files from a specified directory into a single DataFrame and parses it to be saved.
"""
import glob
import pandas as pd
import file_control as fc
# Defining path to the cvs files.
csv_folder = str(fc.get_path())
csv_files = glob.glob(f"{csv_folder}/**/*.csv", recursive = True)

# Read and concatenate CSV files into one.
df_list = []
for file in csv_files:
    temp_df = pd.read_csv(file)
    df_list.append(temp_df)

df = pd.concat(df_list, ignore_index=True)
print("Combined shape:", df.shape)

#Convert datetime column to datetime
df['datetime']= pd.to_datetime(df['datetime'], errors='coerce')

#Sort the dataframe by datetime and site_name
df = df.sort_values(by=['site_name', 'datetime']).reset_index(drop=True)
print("Sorted shape:", df.shape)
print(df.head())
current_name = str("01_long")
df.to_csv(fc.save_path(csv_folder, current_name), index=False)