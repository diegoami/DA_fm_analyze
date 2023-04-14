import pandas as pd


srt_keys = ['Acc', 'Agi', 'Ant', 'Bal', 'Bra', 'Cmp', 'Cnt', 'Cro', 'Dec', 'Dri', 'Fin', 'Fir', 'Fla',
            'Hea', 'Jum', 'Ldr', 'Lon', 'Mar', 'OtB', 'Pac', 'Pas', 'Pos', 'Sta', 'Str', 'Tck', 'Tea',
            'Tec', 'Vis', 'Wor']


ATTRS_TO_ADD = {
    "Aerial Presence" : ['Jum'],
    "Awareness": ['Ant', 'Tea', 'Vis'],
    "Clearing": ['Hea'],
    "Closing Down" : ['Pos', 'Cmp'],
    "Control": ['Fir', 'Tec'],
    "Creativity": ['Ant', 'Dec', 'Fla'],
    "Crossing": ['Cro', 'Pas', 'Tec', 'Cmp'],
    "Decision Making": ['Dec', 'Tea'],
    "Defensive Positioning": ['Pos', 'Cmp'],
    "Dribbling" : ['Dri', 'Tec' ],
    "Focus": ['Cmp', 'Cnt'],
    "Endeavour" : ['Agg', 'Bra', 'Det', 'Wor'],
    "Intelligence" : ['Ant', 'Dec', 'Fla', 'Tea', 'Vis'],
    "Marking" : ['Mar' , 'Cmp', 'Pos'],
    "Mobility" : ['Acc', 'Agi', 'Bal', 'Pac'],
    "Movement" : ['Ant', 'Dec', 'Tea'],
    "Off The Ball" : ['OtB', 'Cmp'],
    "Passing" : ['Pas', 'Tec', 'Cmp'],
    "Physical Presence" : ['Str', 'Bal'],
    "Tackling" : ['Tck', 'Cmp'],

}

def add_attr(sdf, tdf, new_col, cols):
    tdf[new_col] = sdf[cols].mean(axis=1)

def build_instrs(basedir, all_attrs_df):
    inst_df = pd.DataFrame()
    for attr, cols in ATTRS_TO_ADD.items():
        add_attr(all_attrs_df, inst_df, attr, cols)
    inst_df.to_csv(f'{basedir}/insts.csv', index=False)
    return inst_df
