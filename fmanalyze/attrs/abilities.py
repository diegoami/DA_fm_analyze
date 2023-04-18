

srt_keys = ['Acc', 'Agi', 'Ant', 'Bal', 'Bra', 'Cmp', 'Cnt', 'Cro', 'Dec', 'Dri', 'Fin', 'Fir', 'Fla',
            'Hea', 'Jum', 'Ldr', 'Lon', 'Mar', 'OtB', 'Pac', 'Pas', 'Pos', 'Sta', 'Str', 'Tck', 'Tea',
            'Tec', 'Vis', 'Wor']

tecabi_keys = [ "Clearing", "Control", "Crossing", "Dribbling", "Off The Ball", "Passing", "Shooting", "Tackling"]
menabi_keys = [ "Awareness", "Closing", "Creativity", "Decision", "Defensive", "Endeavour",
                "Focus", "Intelligence", "Marking", "Movement"]
phsyabi_keys = [ "Aerial", "Mobility", "Physical" ]

ATTRS_TO_ADD = {
    "Aerial" : ['Jum'],
    "Awareness": ['Ant', 'Tea', 'Vis'],
    "Clearing": ['Hea'],
    "Closing" : ['Pos', 'Cmp'],
    "Control": ['Fir', 'Tec'],
    "Creativity": ['Ant', 'Dec', 'Fla'],
    "Crossing": ['Cro', 'Pas', 'Tec'],
    "Decision": ['Dec', 'Tea'],
    "Defensive": ['Pos', 'Cmp'],
    "Dribbling" : ['Dri', 'Tec' ],
    "Focus": ['Cmp', 'Cnt'],
    "Endeavour" : ['Agg', 'Bra', 'Det', 'Wor'],
    "Intelligence" : ['Ant', 'Dec', 'Fla', 'Tea', 'Vis'],
    "Marking" : ['Mar' , 'Cmp', 'Pos'],
    "Mobility" : ['Acc', 'Agi', 'Bal', 'Pac'],
    "Movement" : ['Ant', 'Dec', 'Tea'],
    "Off The Ball" : ['OtB'],
    "Passing" : ['Pas', 'Tec'],
    "Physical" : ['Str', 'Bal'],
    "Shooting" : ['Fin', 'Lon', 'Tec'],
    "Tackling" : ['Tck'],

}

columns_to_round = list(ATTRS_TO_ADD.keys())

def create_abilities(basedir, df):
    new_df = df[['Player', 'UID']].copy()
    for attr, cols in ATTRS_TO_ADD.items():
        new_df[attr] = df[cols].mean(axis=1)


    new_df[columns_to_round] = new_df[columns_to_round].round(2)
    new_df.to_csv(f'{basedir}/abis.csv', index=False)
    return new_df

def split_abilities(df):
    columns = ['Player', 'UID']
    if "Position" in df.columns:
        columns.append('Position')
    tec_abis = df[columns + tecabi_keys].copy()
    men_abis = df[columns + menabi_keys].copy()
    phys_abis = df[columns + phsyabi_keys].copy()

    return tec_abis, men_abis, phys_abis