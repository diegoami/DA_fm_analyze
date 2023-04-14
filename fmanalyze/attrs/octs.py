


def create_octs(basedir, df):
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
