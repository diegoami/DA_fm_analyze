import os

import pandas as pd


def combine_dfs(targetdir, filename):
    dataframes = {}
    for teams in os.listdir(targetdir):
        attr_file = os.path.join(targetdir, teams, filename)
        if os.path.exists(attr_file):
            dataframes[teams] = pd.read_csv(attr_file)
    # Initialize an empty DataFrame to store the concatenated data
    combined_df = pd.DataFrame()
    # Iterate through the dictionary, adding a new column with the key and concatenating the DataFrames
    for team, df in dataframes.items():
        df_with_key = df.copy()  # Create a copy to avoid modifying the original DataFrames
        df_with_key['Team'] = team  # Add a new column with the key
        combined_df = pd.concat([combined_df, df_with_key], ignore_index=True)
    # The combined_df now contains all the DataFrames with an additional 'key' column
    print(combined_df)
    combined_df.to_csv(os.path.join(targetdir, filename), index=False)
    return combined_df
