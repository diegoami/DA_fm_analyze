
import pandas as pd

basedir='inter'
import pandas as pd

# Define the roles and their corresponding weights for each attribute
weights = {
    'GK': [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 3, 6, 2, 6, 10, 2, 0, 5, 2, 1, 1, 6, 8, 2, 1, 3, 1, 4],
    'DRL': [2, 1, 1, 3, 2, 1, 3, 2, 4, 2, 3, 2, 2, 4, 7, 1, 1, 4, 2, 2, 2, 7, 6, 2, 2, 5, 6, 4],
    'DC': [1, 1, 1, 2, 5, 1, 8, 2, 5, 1, 5, 2, 2, 4, 10, 2, 1, 8, 1, 1, 2, 6, 6, 2, 6, 5, 3, 6],
    'WBRL': [3, 2, 1, 3, 1, 1, 2, 3, 3, 3, 3, 1, 2, 3, 5, 1, 2, 3, 2, 2, 2, 8, 5, 2, 1, 6, 7, 4],
    'DM': [1, 2, 2, 4, 1, 3, 3, 4, 7, 3, 5, 1, 2, 3, 8, 1, 1, 5, 2, 4, 4, 6, 6, 2, 1, 4, 4, 5],
    'MRL': [5, 3, 2, 4, 1, 2, 1, 3, 2, 4, 3, 1, 3, 2, 5, 1, 2, 1, 2, 3, 3, 8, 6, 2, 1, 6, 5, 3],
    'MC': [1, 2, 2, 6, 1, 3, 3, 6, 3, 4, 3, 1, 3, 2, 7, 1, 3, 3, 2, 6, 6, 6, 6, 2, 1, 5, 5, 4],
    'AMRL': [5, 5, 2, 5, 1, 2, 1, 2, 2, 4, 3, 1, 3, 2, 5, 1, 2, 1, 2, 3, 3, 10, 6, 2, 1, 10, 7, 3],
    'AMC' : [1, 3, 3, 5, 1, 3, 1, 4, 2, 5, 3, 1, 3, 2, 6, 1, 3, 2, 2, 6, 3, 9, 6, 2, 1, 7, 6 ,3],
    'SC' : [2, 5, 8, 6, 6, 2, 1, 2, 1, 4, 5, 1, 6, 2, 5, 1, 6, 2, 1, 2, 2, 10, 6, 2, 5, 7, 6, 6]
}

abbr_keys = [
    'Cro', 'Dri', 'Fin', 'Fir', 'Hea', 'Lon', 'Mar', 'Pas',
    'Tck', 'Tec',  'Ant', 'Bra', 'Cmp', 'Cnt', 'Dec',
    'Ldr', 'OtB', 'Pos', 'Tea', 'Vis', 'Wor', 'Acc', 'Agi', 'Bal', 'Jum',
    'Pac', 'Sta', 'Str'
]


with open(f'{basedir}/all_attrs.txt', 'r') as file:
  raw_data = file.readlines()

columns = raw_data[0].strip().strip('|').split('|')
columns = [x.strip() for x in columns]
print(columns)
# Clean the data
cleaned_data = []
for line in raw_data:
  if not line or not 'Pick Player' in line:
    continue
  line = line.strip().replace(" - Pick Player ", "").strip('|')

  cleaned_line = [x.strip() for x in line.split('|')]
  cleaned_data.append(cleaned_line)


df = pd.DataFrame(cleaned_data, columns=columns)
for col in columns[2:]:
  df[col] = df[col].astype(int)


# Calculate weighted sum of attributes for each role
def calculate_weighted_sum(df, new_df, weights):

    for role, weight_values in weights.items():
        new_df[role] = df[abbr_keys].multiply(weight_values, axis=1).sum(axis=1)

    return new_df


import pandas as pd


def calculate_weighted_sum_2(df, new_df, weights):
    for role, weight_values in weights.items():
        print(f"Calculating weighted sum for role: {role}")

        for idx, row in df.iterrows():
            new_df.at[idx, role] = 0
            print(f"  For player {new_df.at[idx, 'Player']}: ")
            idxstr = ""
            for col, weight_value in zip(df.columns, weight_values):
                idxstr += f"'{col}': {weight_value} * "
                idxstr += f" {row[col]} + "
                #idxstr += f"weighted sum: {row[col] * weight_value}, "
                new_df.at[idx, role] += row[col] * weight_value
            print(idxstr)
            print(f"  Total weighted sum for index {idx}: {new_df.at[idx, role]}\n")

    return new_df


new_df = df[['Player', 'UID']]
df_tmp = df[abbr_keys]
# Create the new DataFrame with weighted sums for each role
weighted_sums_df = calculate_weighted_sum_2(df_tmp, new_df,  weights)

# Set the index of the new DataFrame to match the player names from the original DataFrame

print(weighted_sums_df)

weighted_sums_df.to_csv(f'{basedir}/wsums2.txt', index=False)