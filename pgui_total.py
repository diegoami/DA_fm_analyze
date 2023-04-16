import argparse
from pandasgui import show
import pandas
import yaml
from fmanalyze.text import view_parse
from fmanalyze.roles.extract import COL_ROLES

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--config')
    args = parser.parse_args()
    if args.config == None:
        print("required argument --config <config>")
        exit()
    else:
        with open(args.config, 'r') as confhandle:
            config = yaml.safe_load(confhandle)

    basedir = config["target_dir"]
    all_csvs = [f'{role}_attrs' for role in COL_ROLES]
    all_dfs = {}

    for csv in all_csvs:
        csv_df = pandas.read_csv(f'{basedir}/{csv}.csv')
        all_dfs[csv] = csv_df

    #all_dfs = { all_csv : pandas.read_csv(f'{basedir}/{all_csv}.csv') for all_csv in all_csvs}
    gui = show(**all_dfs)