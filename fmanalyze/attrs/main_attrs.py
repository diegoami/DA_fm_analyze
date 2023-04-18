import pandas as pd
import os

tec_keys = ['Cro', 'Dri', 'Fin', 'Fir', 'Hea', 'Lon', 'Mar', 'Pas', 'Tck', 'Tec']
men_keys = ['Ant', 'Bra', 'Cmp', 'Cnt', 'Dec', 'Ldr', 'OtB', 'Pos', 'Tea', 'Vis', 'Wor']
phys_keys = ['Acc', 'Agi', 'Bal', 'Jum', 'Pac', 'Sta', 'Str']


def separate_in_tec_men_phys(df):
    columns = ['Player', 'UID']
    if "Position" in df.columns:
        columns.append('Position')
    tec_df = df[columns + tec_keys].copy()
    men_df = df[columns + men_keys].copy()
    phys_def = df[columns + phys_keys].copy()
    return tec_df, men_df, phys_def


def fill_color_df(df, color_df, quantile_dfs):
    pass
def deal_with_fuzzy_attrs(field):
    if '-' in field:
        first, lst = field.split('-')
        if first.isdigit() and lst.isdigit():
            return round((float(first) + float(lst)) / 2, 2)
        else:
            return 0
    else:
        return field

def parse_attr_list(basedir, overwrite=True):

    last_part = os.path.basename(basedir)
    attr_filename = f'{basedir}/{last_part}.rtf'



    if os.path.isfile(attr_filename) and overwrite:
        with open(attr_filename, 'r', encoding='UTF-8') as file:
            raw_data = [line for line in file.readlines() if line.strip() ]
        print(raw_data)

        columns = raw_data[0].strip().strip('|').split('|')
        columns = [x.strip() for x in columns]
        # Clean the data
        cleaned_data = []
        for line in raw_data:
            if not line or not line.strip() or not 'Pick Player' in line:
                continue
            line = line.strip().replace(" - Pick Player ", "").strip('|')

            cleaned_line = [x.strip() for x in line.split('|')]
            cleaned_line = [deal_with_fuzzy_attrs(x) for x in cleaned_line]
            cleaned_data.append(cleaned_line)
        df = pd.DataFrame(cleaned_data, columns=columns)
        pos_df = df[["Player", "UID", "Position"]].copy()
        df = df.drop(columns=["Position"], axis=1)
        columns = df.columns
        for col in columns[1:]:
            df[col] = df[col].astype(float)
        df.to_csv(f'{basedir}/all_attrs.csv', encoding='UTF-8', index=False)
        pos_df.to_csv(f'{basedir}/pos.csv', encoding='UTF-8', index=False)
        return df, pos_df
    else:
        if os.path.isfile(f'{basedir}/all_attrs.csv'):
            df = pd.read_csv(f'{basedir}/all_attrs.csv')
            if os.path.isfile(f'{basedir}/pos.csv'):
                pos_df = pd.read_csv(f'{basedir}/pos.csv')
                return df, pos_df
            else:
                pos_df = df[["Player", "UID", "Position"]].copy()
                pos_df.to_csv(f'{basedir}/pos.csv', encoding='UTF-8', index=False)
                return df, pos_df
        else:
            print(f'Cannot find {attr_filename}')
            return None, None