import argparse
import os

from fmanalyze.aggregate.collect import create_dfs_for_basedir
from fmanalyze.attrs.instructions import *

pd.options.mode.chained_assignment = None
import yaml
import glob


def create_all_dfs():
    getcwd = os.getcwd()
    data_dir = os.path.join(getcwd, '../../data')
    rtf_files = glob.glob(os.path.join(data_dir, '**/*.rtf'), recursive=True)
    for rtf_file in rtf_files:
        print(f'Processing {rtf_file}...')
        basedir = os.path.dirname(rtf_file)
        create_dfs_for_basedir(basedir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--config', help='Path to config file', default=None, required=False)
    args = parser.parse_args()
    if args.config == None:
        create_all_dfs()
    else:
        with open(args.config, 'r') as confhandle:
            config = yaml.safe_load(confhandle)

        basedir = config["basedir"]

        create_dfs_for_basedir(basedir)