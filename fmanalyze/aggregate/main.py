from fmanalyze.attrs.abilities import create_abilities
from fmanalyze.attrs.instructions import build_instrs
from fmanalyze.attrs.main_attrs import parse_attr_list
from fmanalyze.attrs.octs import create_octs, create_gk_octs
from fmanalyze.attrs.positions import calculate_weighted_sum, weights
from fmanalyze.attrs.roles import create_all_roles
from fmanalyze.roles.extract import evaluate_positions, extract_roles, extract_match_roles


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
