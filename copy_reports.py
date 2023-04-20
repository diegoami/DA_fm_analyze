import argparse
import os

from fmanalyze.attrs.instructions import *
from fmanalyze.aggregate.collect import create_dfs_for_basedir

pd.options.mode.chained_assignment = None
import yaml
import shutil


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--config', help='Path to config file', default=None, required=False)
    args = parser.parse_args()
    with open(args.config, 'r') as confhandle:
        config = yaml.safe_load(confhandle)

    sourcedir = config.get("source_dir", None)
    targetdir = config.get("target_dir", None)

    if sourcedir is not None and targetdir is not None:
        teams_dir = os.path.join(targetdir, 'teams')

        for rtf_filame in os.listdir(sourcedir):
            print(f'Processing {rtf_filame}...')
            dir_to_create = os.path.splitext(rtf_filame)[0]
            basedir = os.path.join(teams_dir, dir_to_create)

            os.makedirs(os.path.join(basedir), exist_ok=True)
            shutil.copyfile(os.path.join(sourcedir, rtf_filame), os.path.join(basedir, rtf_filame))
            print(f'Creating dfs for {basedir}...')

    if targetdir is not None:
        print("Creating dfs for all dirs in targetdir...")
        for dir in os.listdir(teams_dir):
            basedir = os.path.join(teams_dir, dir)
            create_dfs_for_basedir(basedir)