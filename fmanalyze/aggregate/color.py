import pandas as pd

from fmanalyze.roles.utils import convert_position
from fmanalyze.roles.extract import COL_ROLES


def create_color_roles_dfs(league_dir, selected_role=None):
    color_roles_dfs = {}
    if selected_role is not None:
        col_loop_roles = [convert_position(selected_role)]
    else:
        col_loop_roles = COL_ROLES
    for role in col_loop_roles:
        quantile_abi_df_name, quantile_attr_df_name, quantile_octs_df_name, quantile_gk_octs_df_name = \
            f'quantiles_{role}_abis', f'quantiles_{role}_attrs', f'quantiles_{role}_octs', f'quantiles_{role}_gk_octs'
        color_roles_dfs[quantile_abi_df_name] = pd.read_csv(f'{league_dir}/{quantile_abi_df_name}.csv')
        color_roles_dfs[quantile_attr_df_name] = pd.read_csv(f'{league_dir}/{quantile_attr_df_name}.csv')
        color_roles_dfs[quantile_octs_df_name] = pd.read_csv(f'{league_dir}/{quantile_octs_df_name}.csv')
        color_roles_dfs[quantile_gk_octs_df_name] = pd.read_csv(f'{league_dir}/{quantile_gk_octs_df_name}.csv')

    return color_roles_dfs




def fill_color_dfs(color_dfs, all_dfs, color_roles_dfs, selected_role=None):
    color_dfs.update({f'{name}_color': df.copy() for name, df in all_dfs.items()})
    for name, df in color_dfs.items():
        df.loc[:, ~df.columns.isin(["Player", "UID", "Position"])] = 0
    for name, df in all_dfs.items():
        if name in ['tec', 'men', 'phys', 'goalk', 'octs', 'gk_octs', 'tecabi', 'menabi', 'physabi']:
            print("Processing", name)
            for item, row in df.iterrows():
                player, uid = row['Player'], row['UID']
                if not 'Position' in row:
                    print(row)
                position = row['Position']
                position = convert_position(position)
                if name in ['tec', 'men', 'phys', 'goalk']:
                    ref_color_df = color_roles_dfs[f'quantiles_{position}_attrs']
                elif name in ['tecabi', 'menabi', 'physabi']:
                    ref_color_df = color_roles_dfs[f'quantiles_{position}_abis']
                elif name in ['octs']:
                    ref_color_df = color_roles_dfs[f'quantiles_{position}_octs']
                elif name in ['gk_octs']:
                      ref_color_df = color_roles_dfs[f'quantiles_{position}_gk_octs']

                color_df = color_dfs[f'{name}_color']

                for index, ref_color_row in ref_color_df.iterrows():

                    col = ref_color_row['COL']
                    if col in df.columns:
                        if row[col] < ref_color_row['Q20']:
                            color_df.loc[(color_df['UID'] == uid) & (color_df['Position'] == position), col] = -2
                        if row[col] >= ref_color_row['Q20'] and row[col] < ref_color_row['Q40']:
                            color_df.loc[(color_df['UID'] == uid) & (color_df['Position'] == position), col] = -1
                        elif row[col] >= ref_color_row['Q40'] and row[col] < ref_color_row['Q60']:
                            color_df.loc[(color_df['UID'] == uid) & (color_df['Position'] == position), col] = 0
                        elif row[col] >= ref_color_row['Q60'] and row[col] < ref_color_row['Q80']:
                            color_df.loc[(color_df['UID'] == uid) & (color_df['Position'] == position), col] = 1
                        elif row[col] >= ref_color_row['Q80']:
                            color_df.loc[(color_df['UID'] == uid) & (color_df['Position'] == position), col] = 2
