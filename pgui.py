import argparse
from pandasgui import show
import pandas
import yaml
import view_parse

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

    basedir = config["basedir"]
    formation = config["formation"]
    all_csvs = ['all_attrs', 'octs', 'wsums', 'cd', 'fb', 'dm', 'cm', 'wm', 'amc', 'amlr', 'st', 'abis']
    all_dfs = {}
    if formation:
        formation_df = view_parse.parse_selection(basedir)

    for csv in all_csvs:
        csv_df = pandas.read_csv(f'{basedir}/{csv}.csv')
        if formation_df is not None:
            csv_df = formation_df.merge(csv_df, on='UID', how='inner')
        all_dfs[csv] = csv_df

    #all_dfs = { all_csv : pandas.read_csv(f'{basedir}/{all_csv}.csv') for all_csv in all_csvs}
    gui = show(**all_dfs)