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

def read_formation(formation_file):
    #formation_file = os.path.join(formation_dir, 'formation.csv')
    with open(formation_file, 'r', encoding='UTF-8') as file:
        lines = file.readlines()

    filtered_lines = [line for line in lines if not line.startswith('#')]
    data = pd.read_csv(io.StringIO(''.join(filtered_lines)))
    if 'Match' in data.columns:
#        data.drop(columns=['Position'], inplace=True)
        data.rename(columns={'Match': 'Position'}, inplace=True)
    data.sort_values(by=['Position'], inplace=True, key=lambda x: x.map(sort_positions))
    return data
