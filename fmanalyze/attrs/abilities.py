

srt_keys = ['Acc', 'Agi', 'Ant', 'Bal', 'Bra', 'Cmp', 'Cnt', 'Cro', 'Dec', 'Dri', 'Fin', 'Fir', 'Fla',
            'Hea', 'Jum', 'Ldr', 'Lon', 'Mar', 'OtB', 'Pac', 'Pas', 'Pos', 'Sta', 'Str', 'Tck', 'Tea',
            'Tec', 'Vis', 'Wor']


ATTRS_TO_ADD = {
    "Aerial" : ['Jum'],
    "Awareness": ['Ant', 'Tea', 'Vis'],
    "Clearing": ['Hea'],
    "Closing" : ['Pos', 'Cmp'],
    "Control": ['Fir', 'Tec'],
    "Creativity": ['Ant', 'Dec', 'Fla'],
    "Crossing": ['Cro', 'Pas', 'Tec', 'Cmp'],
    "Decision": ['Dec', 'Tea'],
    "Defensive": ['Pos', 'Cmp'],
    "Dribbling" : ['Dri', 'Tec' ],
    "Focus": ['Cmp', 'Cnt'],
    "Endeavour" : ['Agg', 'Bra', 'Det', 'Wor'],
    "Intelligence" : ['Ant', 'Dec', 'Fla', 'Tea', 'Vis'],
    "Marking" : ['Mar' , 'Cmp', 'Pos'],
    "Mobility" : ['Acc', 'Agi', 'Bal', 'Pac'],
    "Movement" : ['Ant', 'Dec', 'Tea'],
    "Off The Ball" : ['OtB', 'Cmp'],
    "Passing" : ['Pas', 'Tec', 'Cmp'],
    "Physical" : ['Str', 'Bal'],
    "Shooting" : ['Fin', 'Lon', 'Tec'],
    "Tackling" : ['Tck', 'Cmp'],

}


def create_abilities(basedir, df):
    new_df = df[['Player', 'UID']]
    for attr, cols in ATTRS_TO_ADD.items():
        new_df[attr] = df[cols].mean(axis=1)

    new_df.to_csv(f'{basedir}/abis.csv', index=False)
    return new_df
