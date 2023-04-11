

from pandasgui import show
import pandas

base_dir = 'rsana'
#new_df = pandas.read_csv('data/octs.txt')
octs_df =  pandas.read_csv(f'{base_dir}/octs.txt')
wsums_df = pandas.read_csv(f'{base_dir}/wsums2.txt')
#attrs_df = pandas.read_csv(f'{base_dir}/all_attrs.txt')
middle_df = pandas.read_csv(f'{base_dir}/middle.txt')
att_df = pandas.read_csv(f'{base_dir}/attack.txt')

# Display the DataFrame in PandasGUI
dfs = {
    "octs" : octs_df,
    "wsums" : wsums_df,
#    "attrs" : attrs_df,
#    "middle" : middle_df,
#    "att" : att_df
}

#gui = show(octs_df)
gui = show(octs_df, wsums_df)