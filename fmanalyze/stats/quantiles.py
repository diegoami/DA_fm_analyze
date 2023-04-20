import pandas
import pandas as pd

from fmanalyze.roles.extract import COL_ROLES


def save_stats_for_attrs(rolesdir, quantilesdir, filesufix):
    all_csvs = [f'{role}_{filesufix}' for role in COL_ROLES]
    all_dfs = {}
    for csv in all_csvs:
        csv_df = pandas.read_csv(f'{rolesdir}/{csv}.csv')
        all_dfs[csv] = csv_df
        quantiles_df = pd.DataFrame(columns=["DF", "COL", "Q0", "Q20", "Q40", "Q60", "Q80", "Q100"])
        print(csv_df.dtypes)
        for col in csv_df.columns:
            if (csv_df[col].dtype == "int64" or csv_df[col].dtype == "float64") and col != "UID":
                new_row = {
                    "DF": csv,
                    "COL": col,
                    "Q0": csv_df[col].quantile(0, interpolation='nearest'),
                    "Q20": csv_df[col].quantile(0.2, interpolation='nearest'),
                    "Q40": csv_df[col].quantile(0.4, interpolation='nearest'),
                    "Q60": csv_df[col].quantile(0.6, interpolation='nearest'),
                    "Q80": csv_df[col].quantile(0.8, interpolation='nearest'),
                    "Q100": csv_df[col].quantile(1, interpolation='nearest')
                }
                quantiles_csv_df_cols = pd.DataFrame([new_row])

                # add a new row to the dataframe
                quantiles_df = pd.concat([quantiles_df, quantiles_csv_df_cols], ignore_index=True)
        print(f"Saving quantiles_{csv}.csv")
        quantiles_df.to_csv(f'{quantilesdir}/quantiles_{csv}.csv')
    # all_dfs = { all_csv : pandas.read_csv(f'{basedir}/{all_csv}.csv') for all_csv in all_csvs}
