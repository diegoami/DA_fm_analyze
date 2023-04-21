import argparse

from fmanalyze.attrs.instructions import *
from fmanalyze.stats.leagues import generate_all_combinations
import os
pd.options.mode.chained_assignment = None
import yaml

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--config', help='Path to config file', default=None, required=False)
    args = parser.parse_args()
    with open(args.config, 'r') as confhandle:
        config = yaml.safe_load(confhandle)

    sourcedir = config.get("source_dir", None)
    targetdir = config.get("target_dir", None)
    if sourcedir is not None and targetdir is not None:

        roledir = os.path.join(targetdir, 'roles')
        teamdir = os.path.join(targetdir, 'teams')
        os.makedirs(roledir, exist_ok=True)
        generate_all_combinations(roledir, teamdir)

