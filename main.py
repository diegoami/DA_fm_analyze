import pandas as pd

basedir = 'rsana'


def parse_df():
    with open('{basedir}/all_attrs.txt', 'r') as file:
        raw_data = file.readlines()
    columns = raw_data[0].strip().strip('|').split('|')
    columns = [x.strip() for x in columns]
    print(columns)
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
    print(new_df)
    columns_to_round = ['Defending', 'Physical', 'Speed', 'Vision', 'Attacking', 'Technical', 'Aerial', 'Mental']
    new_df[columns_to_round] = new_df[columns_to_round].round(2)
    print(new_df)
    new_df.to_csv('{base_dir}/octs.txt', index=False)
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
    print(player_role_df)
    player_role_df = player_role_df.round(2)

    player_role_df.to_csv('{base_dir}/middle.txt', index=False)
    return player_role_df

player_role_df = df[['Player', 'UID']]

# Create an empty DataFrame with the same number of rows as the original DataFrame

# Calculate the average values for each player role
for role, attributes in player_roles_att.items():
    player_role_df[role] = df[attributes].mean(axis=1)

# Round the values to two decimal places

player_role_df.to_csv('data/attack.txt', index=False)


if __name__ == '__main__':
    df = parse_df()
    new_df = create_octs(df)

    player_roles_mf = {
        'DLP': ['Tec', 'Pas', 'Vis', 'Tec', 'Cmp', 'Ant', 'Dec', 'Pos', 'Tea', 'Cnt'],
        'Regista': ['Pas', 'Vis', 'Tec', 'Fir', 'Cro', 'Ant', 'Dec', 'OtB', 'Pos', 'Cnt'],
        'BWM': ['Tck', 'Agg', 'Wor', 'Sta', 'Pos', 'Tea', 'Str', 'Bra', 'Ant', 'Cnt'],
        'BBM': ['Sta', 'Wor', 'Fir', 'Pas', 'Tec', 'OtB', 'Pos', 'Ant', 'Dec', 'Tea'],
        'CM': ['Fir', 'Pas', 'Tec', 'Sta', 'Wor', 'Vis', 'Dec', 'Ant', 'Pos', 'Tea'],
        'AP': ['Fir', 'Pas', 'Vis', 'Tec', 'Cro', 'OtB', 'Ant', 'Dec', 'Cmp', 'Agi'],
        'Mezzala': ['Fir', 'Pas', 'Tec', 'Vis', 'OtB', 'Ant', 'Dec', 'Dri', 'Agi', 'Bal'],
        'Carrilero': ['Wor', 'Sta', 'Pos', 'Tea', 'Ant', 'Tck', 'Dec', 'Fir', 'Pas', 'Cnt']
    }

    player_roles_att = {
        'AF': ['Acc', 'Pac', 'Fin', 'OtB', 'Ant', 'Cmp', 'Dri', 'Agi', 'Bal', 'Sta'],
        'CF': ['Fin', 'Fir', 'Hea', 'Pas', 'Tec', 'OtB', 'Ant', 'Vis', 'Wor', 'Str'],
        'DLF': ['Fir', 'Pas', 'Tec', 'Vis', 'OtB', 'Ant', 'Dec', 'Str', 'Bal', 'Cmp'],
        'F9': ['Fir', 'Pas', 'Tec', 'Vis', 'OtB', 'Ant', 'Dec', 'Dri', 'Bal', 'Cro'],
        'P': ['Fin', 'OtB', 'Ant', 'Acc', 'Pac', 'Cmp', 'Dri', 'Agi', 'Bal', 'Sta'],
        'PF': ['Wor', 'Sta', 'Agg', 'Str', 'Fin', 'OtB', 'Ant', 'Acc', 'Pac', 'Tea'],
        'TM': ['Hea', 'Str', 'Jum', 'Fir', 'Ant', 'Bal', 'OtB', 'Fin', 'Tea', 'Pas']
    }

    create_roles(df, player_roles_mf, 'middle.txt')
    create_roles(df, player_roles_att, 'attack.txt')
