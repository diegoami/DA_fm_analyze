import argparse

import pandas as pd
from pandasgui import show
import pandas
import yaml
import view_parse

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
    "Off The Ball" : ['Otb', 'Cmp'],
    "Passing" : ['Pas', 'Tec', 'Cmp'],
    "Physical Presence" : ['Str', 'Bal'],
    "Tackling" : ['Tck', 'Cmp'],

}

def add_attr(sdf, tdf, new_col, cols):
    tdf[new_col] = sdf[cols].mean(axis=1)


if __name__ == "__main__":
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
    all_attrs_df = pandas.read_csv(f'{basedir}/all_attrs.csv')
    octs_df = pandas.read_csv(f'{basedir}/octs.csv')

    inst_df = pd.DataFrame()
    for attr, cols in ATTRS_TO_ADD.items():
        inst_df[attr] = all_attrs_df[cols].mean(axis=1)
    #add_attr(all_attrs_df, inst_df, )
    inst_df.to_csv(f'{basedir}/insts.csv', index=False)