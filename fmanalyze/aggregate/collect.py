import pandas

from fmanalyze.attrs.abilities import split_abilities
from fmanalyze.attrs.main_attrs import separate_in_tec_men_phys


def fill_all_dfs(all_dfs, basedir, formation_df=None):
    all_octs = pandas.read_csv(f'{basedir}/octs.csv')
    all_attrs = pandas.read_csv(f'{basedir}/all_attrs.csv')
    all_abilities = pandas.read_csv(f'{basedir}/abis.csv')
    if formation_df is not None:
        all_attrs = formation_df.merge(all_attrs, on='UID', how='inner').drop(columns=['Player_y']).rename(
            columns={'Player_x': 'Player'})
        all_abilities = formation_df.merge(all_abilities, on='UID', how='inner').drop(columns=['Player_y']).rename(
            columns={'Player_x': 'Player'})
        all_octs = formation_df.merge(all_octs, on='UID', how='inner').drop(columns=['Player_y']).rename(
            columns={'Player_x': 'Player'})
    all_dfs['octs'] = all_octs
    all_dfs['tec'], all_dfs['men'], all_dfs['phys'] = separate_in_tec_men_phys(all_attrs)
    all_dfs['tecabi'], all_dfs['menabi'], all_dfs['physabi'] = split_abilities(all_abilities)
    for df in all_dfs.values():
        if 'Position' in df.columns:
            temp_column = df.pop('Position')
            df.insert(0, 'Position', temp_column)