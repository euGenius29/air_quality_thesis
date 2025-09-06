"""
This file contains functions for file control operations such as reading, writing and saving new checkpoints.
"""

import glob, os



def get_path():
    """
    Takes the csv folder path from stdin and properly parses it according to the OS.
    Returns the absolute path to the CSV folder.
    """
    import sys

    csv_path = input("Enter the path to the CSV folders: ").strip()
    if not csv_path.endswith('/'):
        csv_path += '/'

    path = os.path.abspath(csv_path)
    if not os.path.isdir(path):
        print(f"Error: {path} is not a valid directory.")
        sys.exit(1)

    return path

def save_path(csv_folder, current_name):
    """
    Generates the path to save the combined DataFrame to a csv file.
    Args:
        csv_folder (str): the folder where the CSV files are located.
        current_name (str): the name to save the combined DataFrame as.
    Returns:
        str: the path where the combined DataFrame is saved.
    """
    current_dir = os.path.dirname(csv_folder)
    # Go up one level to create the saving folder
    parentdir = os.path.dirname(current_dir)

    #Construct the dir path to save the combined csv file.
    target_path = os.path.join(parentdir, "data_processed")
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        print(f"Created directory: {target_path}")
    print(f"Saved to:{target_path} as {current_name}.csv")
    return os.path.join(target_path, f"{current_name}.csv")