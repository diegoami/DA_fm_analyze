import pandas as pd
import argparse

from view_parse import parse_attr_list

pd.options.mode.chained_assignment = None
import yaml


weights = {
    'GK': [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 3, 6, 2, 6, 10, 2, 0, 5, 2, 1, 1, 6, 8, 2, 1, 3, 1, 4],
    'DRL': [2, 1, 1, 3, 2, 1, 3, 2, 4, 2, 3, 2, 2, 4, 7, 1, 1, 4, 2, 2, 2, 7, 6, 2, 2, 5, 6, 4],
    'DC': [1, 1, 1, 2, 5, 1, 8, 2, 5, 1, 5, 2, 2, 4, 10, 2, 1, 8, 1, 1, 2, 6, 6, 2, 6, 5, 3, 6],
    'WBRL': [3, 2, 1, 3, 1, 1, 2, 3, 3, 3, 3, 1, 2, 3, 5, 1, 2, 3, 2, 2, 2, 8, 5, 2, 1, 6, 7, 4],
    'DM': [1, 2, 2, 4, 1, 3, 3, 4, 7, 3, 5, 1, 2, 3, 8, 1, 1, 5, 2, 4, 4, 6, 6, 2, 1, 4, 4, 5],
    'MRL': [5, 3, 2, 4, 1, 2, 1, 3, 2, 4, 3, 1, 3, 2, 5, 1, 2, 1, 2, 3, 3, 8, 6, 2, 1, 6, 5, 3],
    'MC': [1, 2, 2, 6, 1, 3, 3, 6, 3, 4, 3, 1, 3, 2, 7, 1, 3, 3, 2, 6, 6, 6, 6, 2, 1, 5, 5, 4],
    'AMRL': [5, 5, 2, 5, 1, 2, 1, 2, 2, 4, 3, 1, 3, 2, 5, 1, 2, 1, 2, 3, 3, 10, 6, 2, 1, 10, 7, 3],
    'AMC' : [1, 3, 3, 5, 1, 3, 1, 4, 2, 5, 3, 1, 3, 2, 6, 1, 3, 2, 2, 6, 3, 9, 6, 2, 1, 7, 6 ,3],
    'SC' : [2, 5, 8, 6, 6, 2, 1, 2, 1, 4, 5, 1, 6, 2, 5, 1, 6, 2, 1, 2, 2, 10, 6, 2, 5, 7, 6, 6]
}

abbr_keys = [
    'Cro', 'Dri', 'Fin', 'Fir', 'Hea', 'Lon', 'Mar', 'Pas',
    'Tck', 'Tec',  'Ant', 'Bra', 'Cmp', 'Cnt', 'Dec',
    'Ldr', 'OtB', 'Pos', 'Tea', 'Vis', 'Wor', 'Acc', 'Agi', 'Bal', 'Jum',
    'Pac', 'Sta', 'Str'
]


player_roles_mc = {
    'DLP': ['Tec', 'Pas', 'Vis', 'Tec', 'Cmp', 'Ant', 'Dec', 'Pos', 'Tea', 'Cnt'],
    'Regista': ['Pas', 'Vis', 'Tec', 'Fir', 'Cro', 'Ant', 'Dec', 'OtB', 'Pos', 'Cnt'],
    'BWM': ['Tck', 'Agg', 'Wor', 'Sta', 'Pos', 'Tea', 'Str', 'Bra', 'Ant', 'Cnt'],
    'BBM': ['Sta', 'Wor', 'Fir', 'Pas', 'Tec', 'OtB', 'Pos', 'Ant', 'Dec', 'Tea'],
    'CM': ['Fir', 'Pas', 'Tec', 'Sta', 'Wor', 'Vis', 'Dec', 'Ant', 'Pos', 'Tea'],
    'AP': ['Fir', 'Pas', 'Vis', 'Tec', 'Cro', 'OtB', 'Ant', 'Dec', 'Cmp', 'Agi'],
    'Mezzala': ['Fir', 'Pas', 'Tec', 'Vis', 'OtB', 'Ant', 'Dec', 'Dri', 'Agi', 'Bal'],
    'Carrilero': ['Wor', 'Sta', 'Pos', 'Tea', 'Ant', 'Tck', 'Dec', 'Fir', 'Pas', 'Cnt']
}

player_roles_st = {
    'AF': ['Acc', 'Pac', 'Fin', 'OtB', 'Ant', 'Cmp', 'Dri', 'Agi', 'Bal', 'Sta'],
    'CF': ['Fin', 'Fir', 'Hea', 'Pas', 'Tec', 'OtB', 'Ant', 'Vis', 'Wor', 'Str'],
    'DLF': ['Fir', 'Pas', 'Tec', 'Vis', 'OtB', 'Ant', 'Dec', 'Str', 'Bal', 'Cmp'],
    'F9': ['Fir', 'Pas', 'Tec', 'Vis', 'OtB', 'Ant', 'Dec', 'Dri', 'Bal', 'Cro'],
    'P': ['Fin', 'OtB', 'Ant', 'Acc', 'Pac', 'Cmp', 'Dri', 'Agi', 'Bal', 'Sta'],
    'PF': ['Wor', 'Sta', 'Agg', 'Str', 'Fin', 'OtB', 'Ant', 'Acc', 'Pac', 'Tea'],
    'TM': ['Hea', 'Str', 'Jum', 'Fir', 'Ant', 'Bal', 'OtB', 'Fin', 'Tea', 'Pas']
}

player_roles_dm = {
    'DM': ['Tck', 'Mar', 'Pos', 'Ant', 'Cnt', 'Sta', 'Wor', 'Tea', 'Str', 'Dec'],
    'AM': ['Tck', 'Mar', 'Pos', 'Ant', 'Cnt', 'Sta', 'Wor', 'Tea', 'Str', 'Tea'],
    'BWM': ['Tck', 'Mar', 'Pos', 'Ant', 'Cnt', 'Sta', 'Wor', 'Tea', 'Str', 'Tea'],
    'HB': ['Tck', 'Agg', 'Wor', 'Sta', 'Pos', 'Tea', 'Str', 'Bra', 'Ant', 'Cnt'],
    'SV': ['Tck', 'Mar', 'Pos', 'Ant', 'Cnt', 'Sta', 'Wor', 'Fir', 'Pas', 'Cmp'],
    'RGA': ['Pas', 'Vis', 'Tec', 'Fir', 'Fla', 'Ant', 'Dec', 'OtB', 'Pos', 'Cnt']
}

player_roles_cd = {
    'CD': ['Hea', 'Mar', 'Tck', 'Jum', 'Str', 'Pos', 'Ant', 'Cnt', 'Tea', 'Bra'],
    'BPD': ['Hea', 'Mar', 'Tck', 'Jum', 'Str', 'Pos', 'Ant', 'Cnt', 'Fir', 'Pas'],
    'NNCB': ['Hea', 'Mar', 'Tck', 'Jum', 'Str', 'Pos', 'Ant', 'Cnt', 'Bra', 'Agg'],
    'Lib': ['Fir', 'Pas', 'Tec', 'Vis', 'Ant', 'Pos', 'Cnt', 'Tck', 'Mar', 'OtB']
}

player_roles_fb = {
    'FB': ['Tck', 'Mar', 'Pos', 'Ant', 'Cnt', 'Sta', 'Wor', 'Tea', 'Acc', 'Pac'],
    'WB': ['Tck', 'Mar', 'Pos', 'Sta', 'Wor', 'Cro', 'Acc', 'Pac', 'Dri', 'OtB'],
    'IWB': ['Tck', 'Mar', 'Pos', 'Ant', 'Cnt', 'Sta', 'Wor', 'Fir', 'Pas', 'Vis'],
    'CWB': ['Tck', 'Mar', 'Pos', 'Sta', 'Wor', 'Cro', 'Acc', 'Pac', 'Dri', 'OtB', 'Fir', 'Pas', 'Tec'],
    'NNFB': ['Tck', 'Mar', 'Pos', 'Ant', 'Cnt', 'Sta', 'Wor', 'Bra', 'Agg', 'Str']
}

player_roles_wm = {
    'WM': ['Cro', 'Dri', 'Fir', 'Pas', 'Tck', 'Wor', 'Tea', 'Sta', 'Dec', 'OtB'],
    'W': ['Cro', 'Dri', 'Acc', 'Pac', 'Sta', 'Wor', 'Tea', 'OtB', 'Fla', 'Bal'],
    'DW': ['Mar', 'Tck', 'Sta', 'Wor', 'Tea', 'Pos', 'Ant', 'Cnt', 'Cro', 'Pas'],
    'IW': ['Dri', 'Fir', 'Pas', 'Vis', 'Tec', 'Sta', 'Wor', 'OtB', 'Ant', 'Dec'],
    'IF': ['Dri', 'Fin', 'Fir', 'Pas', 'Tec', 'Sta', 'Wor', 'OtB', 'Ant', 'Dec'],
    'WG': ['Cro', 'Dri', 'Acc', 'Pac', 'Sta', 'Wor', 'Tea', 'OtB', 'Fla', 'Bal', 'Hea', 'Jum']
}

player_roles_amc = {
    'AMC': ['Fir', 'Pas', 'Tec', 'Vis', 'Dec', 'Wor', 'Sta', 'Tea', 'OtB', 'Cnt'],
    'AP': ['Fir', 'Pas', 'Tec', 'Vis', 'Fla', 'Dec', 'Wor', 'Sta', 'Tea', 'OtB'],
    'T': ['Fir', 'Pas', 'Tec', 'Vis', 'Dec', 'Wor', 'Sta', 'Tea', 'OtB', 'Cnt'],
    'SS': ['Dri', 'Fin', 'Fir', 'Pas', 'Tec', 'Sta', 'Wor', 'OtB', 'Ant', 'Dec'],
    'AM': ['Dri', 'Fir', 'Pas', 'Vis', 'Tec', 'Sta', 'Wor', 'OtB', 'Ant', 'Dec'],
    'EG': ['Dri', 'Fir', 'Pas', 'Vis', 'Tec', 'Sta', 'Wor', 'OtB', 'Fla', 'Bal']
}

player_roles_amlr = {
    'AML': ['Dri', 'Fir', 'Pas', 'Tec', 'Vis', 'Sta', 'Wor', 'OtB', 'Ant', 'Dec'],
    'AMR': ['Dri', 'Fir', 'Pas', 'Tec', 'Vis', 'Sta', 'Wor', 'OtB', 'Ant', 'Dec'],
    'IW_AML': ['Dri', 'Fir', 'Pas', 'Vis', 'Tec', 'Sta', 'Wor', 'OtB', 'Ant', 'Dec'],
    'IW_AMR': ['Dri', 'Fir', 'Pas', 'Vis', 'Tec', 'Sta', 'Wor', 'OtB', 'Ant', 'Dec'],
    'W_AML': ['Cro', 'Dri', 'Acc', 'Pac', 'Sta', 'Wor', 'Tea', 'OtB', 'Fla', 'Bal'],
    'W_AMR': ['Cro', 'Dri', 'Acc', 'Pac', 'Sta', 'Wor', 'Tea', 'OtB', 'Fla', 'Bal'],
    'IF_AML': ['Dri', 'Fin', 'Fir', 'Pas', 'Tec', 'Sta', 'Wor', 'OtB', 'Ant', 'Dec'],
    'IF_AMR': ['Dri', 'Fin', 'Fir', 'Pas', 'Tec', 'Sta', 'Wor', 'OtB', 'Ant', 'Dec'],
    'WG_AML': ['Cro', 'Dri', 'Acc', 'Pac', 'Sta', 'Wor', 'Tea', 'OtB', 'Fla', 'Bal', 'Hea', 'Jum'],
    'WG_AMR': ['Cro', 'Dri', 'Acc', 'Pac', 'Sta', 'Wor', 'Tea', 'OtB', 'Fla', 'Bal', 'Hea', 'Jum']
}


def create_octs(df):
    # Create a new DataFrame with only the Player and UID columns
    new_df = df[['Player', 'UID']]
    # Calculate the mean of the relevant attributes for each new attribute
    new_df.loc[:, 'Defending'] = df[['Tck', 'Mar', 'Pos']].mean(axis=1)
    new_df.loc[:, 'Physical'] = df[['Str', 'Agi', 'Bal', 'Sta']].mean(axis=1)
    new_df.loc[:, 'Speed'] = df[['Pac', 'Acc']].mean(axis=1)
    new_df.loc[:, 'Vision'] = df[['Pas', 'Tea', 'Fla']].mean(axis=1)
    new_df.loc[:, 'Attacking'] = df[['OtB', 'Fin', 'Cmp']].mean(axis=1)
    new_df.loc[:, 'Technical'] = df[['Tec', 'Fir', 'Dri']].mean(axis=1)
    new_df.loc[:, 'Aerial'] = df[['Jum', 'Hea']].mean(axis=1)
    new_df.loc[:, 'Mental'] = df[['Dec', 'Tea', 'Ant', 'Bra', 'Det', 'Cnt']].mean(axis=1)
    columns_to_round = ['Defending', 'Physical', 'Speed', 'Vision', 'Attacking', 'Technical', 'Aerial', 'Mental']
    new_df[columns_to_round] = new_df[columns_to_round].round(2)
    new_df.to_csv(f'{basedir}/octs.csv', index=False)
    return new_df


def create_roles(df, player_roles, output_file):

    # Create an empty DataFrame with the same number of rows as the original DataFrame
    player_role_df = df[['Player', 'UID']]

    # Calculate the average values for each player role
    # Calculate the average values for each player role
    for role, attributes in  player_roles.items():
        player_role_df[role] = df[attributes].mean(axis=1)
    # Round the values to two decimal places
    player_role_df = player_role_df.round(2)

    player_role_df.to_csv(f'{basedir}/{output_file}', index=False)
    return player_role_df


def calculate_weighted_sum(df,  weights):
    new_df = df[['Player', 'UID']]

    for role, weight_values in weights.items():
        new_df[role] = df[abbr_keys].multiply(weight_values, axis=1).sum(axis=1)
    new_df.to_csv(f'{basedir}/wsums.csv', index=False)
    return new_df



def calculate_weighted_sum_2(df,  weights):
    new_df = df[['Player', 'UID']]

    dfc = df[abbr_keys]

    for role, weight_values in weights.items():
        print(f"Calculating weighted sum for role: {role}")

        for idx, row in df.iterrows():
            new_df.at[idx, role] = 0
            print(f"  For player {new_df.at[idx, 'Player']}: ")
            idxstr = ""
            for col, weight_value in zip(dfc.columns, weight_values):
                idxstr += f"'{col}': {weight_value} * "
                idxstr += f" {row[col]} + "
                #idxstr += f"weighted sum: {row[col] * weight_value}, "
                new_df.at[idx, role] += row[col] * weight_value
            print(idxstr)
            print(f"  Total weighted sum for index {idx}: {new_df.at[idx, role]}\n")

    return new_df

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--config')
    args = parser.parse_args()
    if args.config == None:
        print("required argument --config <config>")
        exit()
    else:
        with open(args.config, 'r') as confhandle:
            config = yaml.safe_load(confhandle)

    basedir = config["basedir"]

    df = parse_attr_list(basedir)
    create_octs(df)

    create_roles(df, player_roles_mc, 'cm.csv')
    create_roles(df, player_roles_st, 'st.csv')
    create_roles(df, player_roles_dm, 'dm.csv')
    create_roles(df, player_roles_cd, 'cd.csv')
    create_roles(df, player_roles_fb, 'fb.csv')
    create_roles(df, player_roles_wm, 'wm.csv')
    create_roles(df, player_roles_amc, 'amc.csv')
    create_roles(df, player_roles_amlr, 'amlr.csv')


    calculate_weighted_sum(df, weights)

