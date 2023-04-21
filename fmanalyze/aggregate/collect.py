import pandas

from fmanalyze.attrs.abilities import split_abilities, create_abilities
from fmanalyze.attrs.instructions import build_instrs
from fmanalyze.attrs.main_attrs import separate_in_tec_men_phys, parse_attr_list
from fmanalyze.attrs.octs import create_octs, create_gk_octs
from fmanalyze.attrs.positions import calculate_weighted_sum, weights
from fmanalyze.attrs.roles import create_all_roles
from fmanalyze.roles.extract import evaluate_positions, extract_roles, extract_match_roles


def fill_all_dfs(all_dfs, basedir, formation_df=None):
    all_octs = pandas.read_csv(f'{basedir}/octs.csv')
    all_gk_octs = pandas.read_csv(f'{basedir}/gk_octs.csv')
    all_attrs = pandas.read_csv(f'{basedir}/all_attrs.csv')
    all_abilities = pandas.read_csv(f'{basedir}/abis.csv')
    if formation_df is not None:
        all_attrs = formation_df.merge(all_attrs, on='UID', how='inner').drop(columns=['Player_y']).rename(
            columns={'Player_x': 'Player'})
        all_abilities = formation_df.merge(all_abilities, on='UID', how='inner').drop(columns=['Player_y']).rename(
            columns={'Player_x': 'Player'})
        all_octs = formation_df.merge(all_octs, on='UID', how='inner').drop(columns=['Player_y']).rename(
            columns={'Player_x': 'Player'})
        all_gk_octs = formation_df.merge(all_gk_octs, on='UID', how='inner').drop(columns=['Player_y']).rename(
            columns={'Player_x': 'Player'})


    all_dfs['octs'] = all_octs
    all_dfs['gk_octs'] = all_gk_octs
    all_dfs['tec'], all_dfs['men'], all_dfs['phys'], all_dfs['goalk'] = separate_in_tec_men_phys(all_attrs)
    all_dfs['tecabi'], all_dfs['menabi'], all_dfs['physabi'] = split_abilities(all_abilities)
    for df in all_dfs.values():
        if 'Position' in df.columns:
            temp_column = df.pop('Position')
            df.insert(0, 'Position', temp_column)


def create_dfs_for_basedir(basedir, overwrite=True):
    df, pos_df = parse_attr_list(basedir, overwrite=overwrite)
    octs_df = create_octs(basedir, df)
    gk_octs_df = create_gk_octs(basedir, df)
    all_roles_df = create_all_roles(basedir, df)
    wsums_df = calculate_weighted_sum(basedir, df, weights)
    evaluate_positions(basedir, pos_df, wsums_df)
    abis_df = create_abilities(basedir, df)
    instrs = build_instrs(basedir, df)
    extract_roles(basedir, pos_df)
    extract_match_roles(basedir)
