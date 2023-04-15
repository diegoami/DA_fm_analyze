import argparse
import yaml
import os
import pandas as pd
from fmanalyze.attrs.positions import weights

COL_ROLES = ['GK', 'DR', 'DC', 'DL', 'WBR', 'DM', 'WBL', 'MR', 'MC', 'ML', 'AMR', 'AMC', 'AML', 'STC']

POS_MAP = {
    'GK': ['GK'],
    'DRL' : ['DR', 'DL'],
    'DC' : ['DC'],
    'WBRL' : ['WBR', 'WBL'],
    'DM' : ['DM'],
    'MRL' : ['MR', 'ML'],
    'AMRL' : ['AMR', 'AML'],
    'ST' : ['STC'],
    'MC' : ['MC'],
    'AMC' : ['AMC']
}

def expand_position(position, suffix):
    return [p.strip() + suffix for p in position.split('/')]

def transform(input_str):
    comma_parts = [part.strip() for part in input_str.split(',')]
    result = []

    for comma_part in comma_parts:
        if ' ' not in comma_part:
            result.append(comma_part)
            continue
        else:
            roles, sides = comma_part.split(' ')
            for poss_side in ['R', 'L', 'C']:
                for role in roles.split('/'):
                    if poss_side in sides:
                        result.append(role + poss_side)
    return result


def do_extract(basedir, pos_df=None):
    roles_df = pos_df[['Player','UID']].copy()
    # Add COL_ROLES to roles_df's columns
    for col in COL_ROLES:
        roles_df[col] = None

    # Iterate Rows in pos_df
    for index, row in pos_df.iterrows():
        position = row['Position']
        poses = transform(position)
        for pos in poses:
            print(f'roles_df.loc[{index}, {pos}]')
            roles_df.loc[index, pos] = 1
    roles_df.fillna(0, inplace=True)
    for col in COL_ROLES:
        roles_df[col] = roles_df[col].astype(int)

    roles_df.to_csv(os.path.join(basedir, 'roles.csv'), index=False)


def do_expand(basedir, pos_df, wsums_df):
    exp_df = pos_df[['Player','UID']].copy()
    for index, row in wsums_df.iterrows():
        for col in wsums_df.columns:
            if col in POS_MAP:
                expanded_poses = POS_MAP[col]
                for expanded_pos in expanded_poses:
                    exp_df.loc[index, expanded_pos] = row[col]
    exp_df.to_csv(os.path.join(basedir, 'exp.csv'), index=False)
