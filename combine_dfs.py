import argparse

from fmanalyze.attrs.instructions import *
from fmanalyze.stats.teams import combine_dfs
from fmanalyze.roles.extract import COL_ROLES
import os
pd.options.mode.chained_assignment = None
import yaml

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--config', help='Path to config file', default=None, required=False)
    args = parser.parse_args()
    with open(args.config, 'r') as confhandle:
        config = yaml.safe_load(confhandle)

    sourcedir = config["source_dir"]
    targetdir = config["target_dir"]


    league_attrs = combine_dfs(targetdir, 'all_attrs.csv')
    league_octs = combine_dfs(targetdir, 'octs.csv')
    league_abis = combine_dfs(targetdir, 'abis.csv')
    league_exps = combine_dfs(targetdir, 'exp.csv')
    league_roles = combine_dfs(targetdir, 'roles.csv')


    for role in COL_ROLES:
        league_players_in_role = league_roles[league_roles[role] == 1][['Player', 'UID', 'Team']]

        league_attrs_in_role = league_attrs.merge(league_players_in_role, on=['Player', 'UID', 'Team'])
        league_attrs_in_role.to_csv(os.path.join(targetdir, f'{role}_attrs.csv'), index=False)

        league_octs_in_role = league_octs.merge(league_players_in_role, on=['Player', 'UID', 'Team'])
        league_octs_in_role.to_csv(os.path.join(targetdir, f'{role}_octs.csv'), index=False)

        league_abis_in_role = league_abis.merge(league_players_in_role, on=['Player', 'UID', 'Team'])
        league_abis_in_role.to_csv(os.path.join(targetdir, f'{role}_abis.csv'), index=False)

        league_exps_in_role = league_exps.merge(league_players_in_role, on=['Player', 'UID', 'Team'])
        league_exps_in_role.to_csv(os.path.join(targetdir, f'{role}_exps.csv'), index=False)

