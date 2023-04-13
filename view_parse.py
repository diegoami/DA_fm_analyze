import pandas as pd
import os


def parse_selection(basedir):
    if not os.path.isfile(f'{basedir}/csel.csv'):
        return None

    with open(f'{basedir}/csel.txt', 'r', encoding='UTF-8') as file:
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


def deal_with_fuzzy_attrs(field):
    if '-' in field:
        first, lst = field.split('-')
        if first.isdigit() and lst.isdigit():
            return round((int(first) + int(lst)) / 2)
        else:
            return field
    else:
        return field

def parse_attr_list(basedir):
    if os.path.isfile(f'{basedir}/all_attrs.csv'):
        df = pd.read_csv(f'{basedir}/all_attrs.csv')
        return df
    else:
        with open(f'{basedir}/all_attrs.txt', 'r', encoding='UTF-8') as file:
            raw_data = [line for line in file.readlines() if line.strip() ]
        print(raw_data)

        columns = raw_data[0].strip().strip('|').split('|')
        columns = [x.strip() for x in columns]
        # Clean the data
        cleaned_data = []
        for line in raw_data:
            if not line or not 'Pick Player' in line:
                continue
            line = line.strip().replace(" - Pick Player ", "").strip('|')

            cleaned_line = [x.strip() for x in line.split('|')]
            cleaned_line = [deal_with_fuzzy_attrs(x) for x in cleaned_line]
            cleaned_data.append(cleaned_line)
        df = pd.DataFrame(cleaned_data, columns=columns)
        for col in columns[1:]:
            df[col] = df[col].astype(int)
        df.to_csv(f'{basedir}/all_attrs.csv', encoding='UTF-8', index=False)
        return df
