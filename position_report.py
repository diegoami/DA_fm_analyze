import argparse
import pandas as pd
import os
from fmanalyze.roles.extract import do_extract, COL_ROLES

pd.options.mode.chained_assignment = None
import yaml




if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--config', help='Path to config file', default=None, required=False)
    args = parser.parse_args()
    with open(args.config, 'r') as confhandle:
        config = yaml.safe_load(confhandle)

    basedir = config["basedir"]
    roles_df = pd.read_csv(os.path.join(basedir, 'roles.csv'))
    wsums = pd.read_csv(os.path.join(basedir, 'wsums.csv'))

    for col in COL_ROLES:
        # finds the rows where the role is not 0

        ps = roles_df[roles_df[col] != 0]
        print(f"{col}: {len(ps)}")