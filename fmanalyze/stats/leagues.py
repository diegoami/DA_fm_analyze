import os

import pandas as pd

from fmanalyze.roles.extract import COL_ROLES


def combine_dfs(teamdir, roledir, filename):
    dataframes = {}
    for teams in os.listdir(teamdir):
        attr_file = os.path.join(teamdir, teams, filename)
        if os.path.exists(attr_file):
            dataframes[teams] = pd.read_csv(attr_file)
    # Initialize an empty DataFrame to store the concatenated data
    combined_df = pd.DataFrame()
    # Iterate through the dictionary, adding a new column with the key and concatenating the DataFrames
    for team, df in dataframes.items():
        df_with_key = df.copy()  # Create a copy to avoid modifying the original DataFrames
        df_with_key['Team'] = team  # Add a new column with the key
        combined_df = pd.concat([combined_df, df_with_key], ignore_index=True)
    # The combined_df now contains all the DataFrames with an additional 'key' column
    combined_df.to_csv(os.path.join(roledir, filename), index=False)

    return combined_df


def generate_combin_for_roles(role, league_attrs, league_octs, league_gk_octs, league_abis, league_roles, roledir):

    league_players_in_role = league_roles[league_roles[role] == 1][['Player', 'UID', 'Team']]

    league_attrs_in_role = league_attrs.merge(league_players_in_role, on=['Player', 'UID', 'Team'])
    league_attrs_in_role.to_csv(os.path.join(roledir, f'{role}_attrs.csv'), index=False)

    league_octs_in_role = league_octs.merge(league_players_in_role, on=['Player', 'UID', 'Team'])
    league_octs_in_role.to_csv(os.path.join(roledir, f'{role}_octs.csv'), index=False)

    league_gk_octs_in_role = league_gk_octs.merge(league_players_in_role, on=['Player', 'UID', 'Team'])
    league_gk_octs_in_role.to_csv(os.path.join(roledir, f'{role}_gk_octs.csv'), index=False)

    league_abis_in_role = league_abis.merge(league_players_in_role, on=['Player', 'UID', 'Team'])
    league_abis_in_role.to_csv(os.path.join(roledir, f'{role}_abis.csv'), index=False)

    league_roles_in_role = league_roles.merge(league_players_in_role, on=['Player', 'UID', 'Team'])
    league_roles_in_role.to_csv(os.path.join(roledir, f'{role}_roles.csv'), index=False)


def generate_all_combinations(roledir, teamdir):
    league_attrs = combine_dfs(teamdir, roledir, 'all_attrs.csv')
    league_octs = combine_dfs(teamdir, roledir, 'octs.csv')
    league_gk_octs = combine_dfs(teamdir, roledir, 'gk_octs.csv')

    league_abis = combine_dfs(teamdir, roledir, 'abis.csv')
    #league_exps = combine_dfs(teamdir, roledir, 'exp.csv')
    league_roles = combine_dfs(teamdir, roledir, 'roles.csv')
    print("Combined all dfs")
    for role in COL_ROLES:
        print("Generating combinations for role: ", role)
        generate_combin_for_roles(role, league_attrs, league_octs, league_gk_octs, league_abis, league_roles, roledir)
