import argparse
import pandas as pd
import os
from fmanalyze.roles.extract import do_extract

pd.options.mode.chained_assignment = None
import yaml




if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--config', help='Path to config file', default=None, required=False)
    args = parser.parse_args()
    with open(args.config, 'r') as confhandle:
        config = yaml.safe_load(confhandle)

    basedir = config["basedir"]
    pos_df = pd.read_csv(os.path.join(basedir, 'pos.csv'))
    do_extract(basedir, pos_df)
