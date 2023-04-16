abbr_keys = [
    'Cro', 'Dri', 'Fin', 'Fir', 'Hea', 'Lon', 'Mar', 'Pas',
    'Tck', 'Tec',  'Ant', 'Bra', 'Cmp', 'Cnt', 'Dec',
    'Ldr', 'OtB', 'Pos', 'Tea', 'Vis', 'Wor', 'Acc', 'Agi', 'Bal', 'Jum',
    'Pac', 'Sta', 'Str'
]


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
    'ST' : [2, 5, 8, 6, 6, 2, 1, 2, 1, 4, 5, 1, 6, 2, 5, 1, 6, 2, 1, 2, 2, 10, 6, 2, 5, 7, 6, 6]
}


def calculate_weighted_sum(basedir, df,  weights):
    new_df = df[['Player', 'UID']]

    for role, weight_values in weights.items():
        sum_weights = sum(weight_values)
        weight_values_l = [x / sum_weights for x in weight_values]
        new_df[role] = df[abbr_keys].multiply(weight_values_l, axis=1).sum(axis=1)
    # Rounds all values to 2 decimals
    new_df = new_df.round(2)
    new_df.to_csv(f'{basedir}/wsums.csv', index=False)

    return new_df



def calculate_weighted_sum_2(basedir, df,  weights):
    new_df = df[['Player', 'UID']]

    dfc = df[abbr_keys]

    for role, weight_values in weights.items():
        print(f"Calculating weighted sum for role: {role}")
        sum_weights = sum(weight_values)
        weight_values_l = [x / sum_weights for x in weight_values]

        for idx, row in df.iterrows():
            new_df.at[idx, role] = 0
            print(f"  For player {new_df.at[idx, 'Player']}: ")
            idxstr = ""
            for col, weight_value_l in zip(dfc.columns, weight_values_l):
                idxstr += f"'{col}': {weight_value_l} * "
                idxstr += f" {row[col]} + "
                #idxstr += f"weighted sum: {row[col] * weight_value}, "
                new_df.at[idx, role] += row[col] * weight_value_l
            print(idxstr)
            print(f"  Total weighted sum for index {idx}: {new_df.at[idx, role]}\n")
    new_df = new_df.round(2)

    new_df.to_csv(f'{basedir}/wsums2.csv', index=False)
    return new_df
