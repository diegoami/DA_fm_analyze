import argparse
import pandas as pd
import os
from fmanalyze.roles.extract import extract_match_roles

pd.options.mode.chained_assignment = None
import yaml

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--config', help='Path to config file', default=None, required=False)
    args = parser.parse_args()
    with open(args.config, 'r') as confhandle:
        config = yaml.safe_load(confhandle)
    basedir = config["basedir"]
    team = config.get("team", None)
    if team:
        teams_dir = os.path.join(basedir, 'teams', team)
        full_df = extract_match_roles(teams_dir)
    else:
        for team in os.listdir(os.path.join(basedir, 'teams')):
            teams_dir = os.path.join(basedir, 'teams', team)
            full_df = extract_match_roles(teams_dir)