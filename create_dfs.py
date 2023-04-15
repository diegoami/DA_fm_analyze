import argparse
import os

from fmanalyze.attrs.octs import create_octs
from fmanalyze.text.view_parse import parse_attr_list
from fmanalyze.attrs.roles import *
from fmanalyze.attrs.positions import *
from fmanalyze.attrs.abilities import create_abilities
from fmanalyze.attrs.instructions import *

pd.options.mode.chained_assignment = None
import yaml
import glob


def create_all_dfs():
    getcwd = os.getcwd()
    data_dir = os.path.join(getcwd, 'data')
    rtf_files = glob.glob(os.path.join(data_dir, '**/*.rtf'), recursive=True)
    for rtf_file in rtf_files:
        print(f'Processing {rtf_file}...')
        basedir = os.path.dirname(rtf_file)
        create_dfs_for_basedir(basedir)


def create_dfs_for_basedir(basedir, overwrite=True):
    df = parse_attr_list(basedir, overwrite=overwrite)
    octs_df = create_octs(basedir, df)
    all_roles_df = create_all_roles(basedir, df)
    wsums_df = calculate_weighted_sum(basedir, df, weights)
    abis_df = create_abilities(basedir, df)
    instrs = build_instrs(basedir, df)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--config', help='Path to conf  ig file', default=None, required=False)
    args = parser.parse_args()
    if args.config == None:
        create_all_dfs()
    else:
        with open(args.config, 'r') as confhandle:
            config = yaml.safe_load(confhandle)

        basedir = config["basedir"]

        create_dfs_for_basedir(basedir)