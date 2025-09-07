'''
This module provides functions for exploratory data analysis (EDA) on a given DataFrame.
'''
import pandas as pd
import file_control as fc
import data_merging as dm
import matplotlib.pyplot as plt
import seaborn as sns

# Load the csv to be analyzed.
def monthly_counts(df):
    """
    Provides monthly counts of non-missing values for each site in the DataFrame.
    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    Returns:
        None
    """
    df = df.copy()
    # Resample the DataFrame to monthly frequency and count non-missing values for each site
    total_rows = df.resample('ME').size().rename('Total Rows')
    missing_values = df.isna().resample('ME').sum()

    combined_df = pd.concat([total_rows, missing_values], axis=1)

    return combined_df

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

    rows_per_month = df.resample('ME').size()
    print("\nNumber of rows per month:\n", rows_per_month)
    #print("\nRows per month statistics:\n", rows_per_month.describe())

    print("\nNumber of rows per month and missing values per month for each site:")
    monthly_counts_df = monthly_counts(df)
    print(monthly_counts_df)
    monthly_counts_df.to_csv(fc.save_path(dm.csv_folder, "monthly_counts"), index=True)



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

def quarterly_divisions_plots(df):
    """
    Analyzes missing data in the DataFrame on a quarterly basis.
    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    Returns:
        None
    """

    df.index = pd.to_datetime(df.index)
    start_date = df.index.min().date()
    end_date = df.index.max().date()
    tz = df.index.tz

    # Generate quarterly periods
    quarters = pd.date_range(start=start_date, end=end_date, freq='QS-JAN', tz=tz)

    for i, quarter_start in enumerate(quarters):
        quarter_end = quarter_start + pd.DateOffset(months=3) - pd.DateOffset(days=1)

        quarterly_df = df.loc[quarter_start:quarter_end]
        if quarterly_df.empty:
            continue

        quarter_label = f"Q{quarterly_df.index[0].quarter} {quarterly_df.index[0].year}"

        # Missing data heatmap (time vs sites) for the quarter
        print(f"\nMissing Data Heatmap for {quarter_label}:")
        plt.figure(figsize=(15,6))
        sns.heatmap(df.isna().T, cmap="viridis", cbar=False)
        plt.title("Missing Data Heatmap (sites vs time) - {quarter_label}")
        plt.xlabel("Time")
        plt.ylabel("Sites")
        plt.show()

        # Plot percentage of sites missing data over time for the quarter
        row_missing = quarterly_df.isna().mean(axis=1) * 100
        plt.figure(figsize=(12,4))
        row_missing.plot()
        plt.ylabel("% Sites Missing")
        plt.title(f"Missing Data Over Time (Network-wide) - {quarter_label}")
        plt.show()