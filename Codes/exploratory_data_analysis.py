'''
This module provides functions for exploratory data analysis (EDA) on a given DataFrame.
'''
import pandas as pd
import file_control as fc
import matplotlib.pyplot as plt
import seaborn as sns

# Load the csv to be analyzed.
def data_description(df):
    """
    Provides a general description on the given DataFrame.
    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    Returns:
        None
    """
    df = df.copy()

    # Basic info about the DataFrame
    print("DataFrame info:")
    print(df.info())
    print("DataFrame shape:", df.shape)
    print("First few rows of the DataFrame:\n", df.head())
    print("Columns in the DataFrame:", df.columns.tolist())
    print("Total unique sites:", df['site_id'].nunique())
    print("Last few rows of the DataFrame:\n", df.tail())

    #Time range of the data
    print("\nTime range of the data:")
    print("\nOldest datetime:", df.index.min())
    print("\nNewest datetime:", df.index.max())
    print("\nTotal Hours:", df.index.max() - df.index.min())

    # General overview and statistics of the DataFrame
    print("\nStatistical summary of the DataFrame:")

    print("\nDescriptive statistics:\n")
    print(df.describe().T)

    fc.duplicate_check(df)
    freq = pd.infer_freq(df.index)
    print(f"\nInferred frequency of the datetime index: {freq}")

    rows_per_month = df.resample('M').size()
    print("\nNumber of rows per month:\n", rows_per_month)
    print("\nRows per month statistics:\n", rows_per_month.describe())


def missing_data_analysis(df):
    """
    Analyzes missing data in the DataFrame.
    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    Returns:
        None
    """
    # Calculate the number and percentage of missing values for each column
    missing_counts = df.isnull().sum()
    missing_percent = df.isna().mean() * 100

    # Combine counts and percentages into a single DataFrame for better visualization
    missing_data = pd.DataFrame({
        'Missing Count': missing_counts,
        'Missing Percentage': missing_percent
    })

    # Filter out columns with no missing data
    missing_data = missing_data[missing_data['Missing Count'] > 0]

    # Sort by percentage of missing data in descending order
    missing_data = missing_data.sort_values(by='Missing Percentage', ascending=False)

    print("\nMissing Data Analysis:")
    print(missing_data)

    # Identify rows with any missing values
    rows_with_missing = df[df.isnull().any(axis=1)]
    print(f"\nTotal rows with any missing values: {len(rows_with_missing)}")
    if not rows_with_missing.empty:
        print("Sample rows with missing values:\n", rows_with_missing.head())

    # Visualize missing data per site using a heatmap
    plt.figure(figsize=(12,5))
    missing_percent.sort_values(ascending=False).plot(kind='bar', color='skyblue')
    plt.ylabel("% Missing")
    plt.title("Percentage of Missing Data per Site")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    # Missing data heatmap (time vs sites)
    plt.figure(figsize=(15,6))
    sns.heatmap(df.isna().T, cmap="viridis", cbar=False)
    plt.title("Missing Data Heatmap (sites vs time)")
    plt.xlabel("Time")
    plt.ylabel("Sites")
    plt.show()

    # Plot percentage of sites missing data over time
    row_missing = df.isna().mean(axis=1) * 100
    plt.figure(figsize=(12,4))
    row_missing.plot()
    plt.ylabel("% Sites Missing")
    plt.title("Missing Data Over Time (Network-wide)")
    plt.show()
