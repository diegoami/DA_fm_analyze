import pandas as pd

basedir = 'inter'


def parse_df():
    with open(f'{basedir}/all_attrs.txt', 'r') as file:
        raw_data = file.readlines()
    columns = raw_data[0].strip().strip('|').split('|')
    columns = [x.strip() for x in columns]
    # Clean the data
    cleaned_data = []
    for line in raw_data:
        if not line or not 'Pick Player' in line:
            continue
        line = line.strip().replace(" - Pick Player ", "").strip('|')

        cleaned_line = [x.strip() for x in line.split('|')]
        cleaned_data.append(cleaned_line)
    df = pd.DataFrame(cleaned_data, columns=columns)
    for col in columns[2:]:
        df[col] = df[col].astype(int)
    return df


def create_octs(df):
    # Create a new DataFrame with only the Player and UID columns
    new_df = df[['Player', 'UID']]
    # Calculate the mean of the relevant attributes for each new attribute
    new_df['Defending'] = df[['Tck', 'Mar', 'Pos']].mean(axis=1)
    new_df['Physical'] = df[['Str', 'Agi', 'Bal', 'Sta']].mean(axis=1)
    new_df['Speed'] = df[['Pac', 'Acc']].mean(axis=1)
    new_df['Vision'] = df[['Pas', 'Tea', 'Fla']].mean(axis=1)
    new_df['Attacking'] = df[['OtB', 'Fin', 'Cmp']].mean(axis=1)
    new_df['Technical'] = df[['Tec', 'Fir', 'Dri']].mean(axis=1)
    new_df['Aerial'] = df[['Jum', 'Hea']].mean(axis=1)
    new_df['Mental'] = df[['Dec', 'Tea', 'Ant', 'Bra', 'Det', 'Cnt']].mean(axis=1)
    columns_to_round = ['Defending', 'Physical', 'Speed', 'Vision', 'Attacking', 'Technical', 'Aerial', 'Mental']
    new_df[columns_to_round] = new_df[columns_to_round].round(2)
    new_df.to_csv(f'{basedir}/octs.txt', index=False)
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

if __name__ == '__main__':
    df = parse_df()
    new_df = create_octs(df)

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
        'DM' : ['Tck', 'Mar', 'Pos', 'Ant', 'Cnt', 'Sta', 'Wor', 'Tea', 'Str', 'Dec'],
        'AM' : ['Tck', 'Mar', 'Pos', 'Ant', 'Cnt', 'Sta', 'Wor', 'Tea', 'Str', 'Tea'],
        'BWM': ['Tck', 'Mar', 'Pos', 'Ant', 'Cnt', 'Sta', 'Wor', 'Tea', 'Str', 'Tea'],
        'HB' : ['Tck', 'Agg', 'Wor', 'Sta', 'Pos', 'Tea', 'Str', 'Bra', 'Ant', 'Cnt'],
        'SV' : ['Tck', 'Mar', 'Pos', 'Ant', 'Cnt', 'Sta', 'Wor', 'Fir', 'Pas', 'Cmp'],
        'RGA' : ['Pas', 'Vis', 'Tec', 'Fir', 'Fla', 'Ant', 'Dec', 'OtB', 'Pos', 'Cnt']
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
    create_roles(df, player_roles_mc, 'middle.txt')
    create_roles(df, player_roles_st, 'attack.txt')
    create_roles(df, player_roles_dm, 'dm.txt')
    create_roles(df, player_roles_cd, 'cd.txt')
    create_roles(df, player_roles_fb, 'fb.txt')
    create_roles(df, player_roles_wm, 'wm.txt')
    create_roles(df, player_roles_amc, 'amc.txt')
    create_roles(df, player_roles_amlr, 'amlr.txt')
