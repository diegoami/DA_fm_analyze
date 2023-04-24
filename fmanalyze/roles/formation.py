import pandas as pd
import os
import io
from fmanalyze.roles.utils import sort_positions
def parse_selection(basedir):
    if not os.path.isfile(f'{basedir}/csel.csv'):
        print("Cannot find csel.csv")
        return None

    with open(f'{basedir}/csel.csv', 'r', encoding='UTF-8') as file:
        raw_data = file.readlines()
    columns = raw_data[0].strip().strip('|').split('|')
    columns = [x.strip() for x in columns]
    cleaned_data = []

    for index, line in enumerate(raw_data):
        if index == 0:
            continue
        if "----" in line:
            continue

        line = line.strip().replace(" - Pick Player ", "").strip('|')
        cleaned_line = [x.strip() for x in line.split('|')]
        if len(cleaned_line) < 2:
            continue
        if len(cleaned_line[0]) < 2:
            continue
        cleaned_data.append(cleaned_line)


    df = pd.DataFrame(cleaned_data, columns=columns)
    df["UID"] = df["UID"].astype(int)
    df.drop(columns=["Name"], inplace=True, axis=1)
    return df


def read_full_formation(formation_dir, formation_file):
    formation_full_file = os.path.join(formation_dir, formation_file)
    data = pd.read_csv(formation_full_file)
    fdata = data[['Player', 'UID']].drop_duplicates()
    fdata['Surname'] = fdata['Player'].apply(lambda name: name.split(' ')[-1])
    fdata = fdata.sort_values(by=['Surname']).drop(columns=['Surname'])
    result_dict = {k: v for k, v in zip(fdata['UID'], fdata['Player'])}
    return result_dict

def read_formation(formation_dir, formation_file, full_formation = False, selected_role = None):
    formation_full_file = os.path.join(formation_dir, formation_file)
    with open(formation_full_file, 'r', encoding='UTF-8') as file:
        lines = file.readlines()
    if full_formation:
        filtered_lines = [line.replace('#','') for line in lines]

    else:
        filtered_lines = [line for line in lines if not line.startswith('#')]

    data = pd.read_csv(io.StringIO(''.join(filtered_lines)))
    if 'Match' in data.columns:
#        data.drop(columns=['Position'], inplace=True)
        data.rename(columns={'Match': 'Position'}, inplace=True)
    data.sort_values(by=['Position'], inplace=True, key=lambda x: x.map(sort_positions))
    if selected_role is not None:
        data = data[data['Position'] == selected_role]
    return data

def save_formation(basedir, df):
    with open(os.path.join(basedir, 'full_formation.csv'), 'w', encoding='UTF-8') as file:
        header = f"{','.join(df.columns)}\n"
        file.write(header)

        # Write rows with '#' at the beginning
        for index, row in df.iterrows():
            formatted_row = f"#{','.join(row.astype(str))}\n"
            file.write(formatted_row)