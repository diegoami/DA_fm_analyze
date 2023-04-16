
GK_Attrs = ["Aer","Cmd","Com","Ecc","Han","Kic","Pun","1v1","Ref","TRO","Thr"]

def create_octs(basedir, df):
    # Create a new DataFrame with only the Player and UID columns
    new_df = df[['Player', 'UID']].copy()
    # Calculate the mean of the relevant attributes for each new attribute
    new_df.loc[:, 'Defending'] = df[['Tck', 'Mar', 'Pos']].mean(axis=1)
    new_df.loc[:, 'Physical'] = df[['Str', 'Agi', 'Bal', 'Sta']].mean(axis=1)
    new_df.loc[:, 'Speed'] = df[['Pac', 'Acc']].mean(axis=1)
    new_df.loc[:, 'Vision'] = df[['Pas', 'Vis', 'Fla']].mean(axis=1)
    new_df.loc[:, 'Attacking'] = df[['OtB', 'Fin', 'Cmp']].mean(axis=1)
    new_df.loc[:, 'Technical'] = df[['Tec', 'Fir', 'Dri']].mean(axis=1)
    new_df.loc[:, 'Aerial'] = df[['Jum', 'Hea']].mean(axis=1)
    new_df.loc[:, 'Mental'] = df[['Dec', 'Tea', 'Ant', 'Bra', 'Det', 'Cnt']].mean(axis=1)
    columns_to_round = ['Defending', 'Physical', 'Speed', 'Vision', 'Attacking', 'Technical', 'Aerial', 'Mental']
    new_df[columns_to_round] = new_df[columns_to_round].round(2)
    new_df.to_csv(f'{basedir}/octs.csv', index=False)
    return new_df

def create_gk_octs(basedir, df):
    # Create a new DataFrame with only the Player and UID columns
    new_df = df[['Player', 'UID']].copy()
    # Calculate the mean of the relevant attributes for each new attribute
    new_df.loc[:, 'Shot Stopping'] = df[['1v1', 'Ref']].mean(axis=1)
    new_df.loc[:, 'Physical'] = df[['Str', 'Agi', 'Bal', 'Sta']].mean(axis=1)
    new_df.loc[:, 'Speed'] = df[['Pac', 'Acc']].mean(axis=1)
    new_df.loc[:, 'Mental'] = df[['Dec', 'Tea', 'Ant', 'Bra', 'Det', 'Cnt']].mean(axis=1)
    new_df.loc[:, 'Communication'] = df[['Cmd', 'Com']].mean(axis=1)
    new_df.loc[:, 'Eccentricity'] = df[['Ecc']].mean(axis=1)
    new_df.loc[:, 'Aerial'] = df[['Aer', 'Han']].mean(axis=1)
    new_df.loc[:, 'Distribution'] = df[['Kic', 'Thr']].mean(axis=1)
    columns_to_round = ['Shot Stopping', 'Physical', 'Speed', 'Mental', 'Communication', 'Eccentricity', 'Aerial', 'Distribution']
    new_df[columns_to_round] = new_df[columns_to_round].round(2)
    new_df.to_csv(f'{basedir}/gk_octs.csv', index=False)
    return new_df
