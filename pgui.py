

from pandasgui import show
import pandas

base_dir = 'inter'
octs_df =  pandas.read_csv(f'{base_dir}/octs.txt')
wsums_df = pandas.read_csv(f'{base_dir}/wsums2.txt')
middle_df = pandas.read_csv(f'{base_dir}/middle.txt')
att_df = pandas.read_csv(f'{base_dir}/attack.txt')
dm_df = pandas.read_csv(f'{base_dir}/dm.txt')
cd_df = pandas.read_csv(f'{base_dir}/cd.txt')
fb_df = pandas.read_csv(f'{base_dir}/fb.txt')
wm_df = pandas.read_csv(f'{base_dir}/wm.txt')
amc_df = pandas.read_csv(f'{base_dir}/amc.txt')
amlr_df = pandas.read_csv(f'{base_dir}/amlr.txt')


# Display the DataFrame in PandasGUI
dfs = {
    "octs" : octs_df,
    "wsums" : wsums_df,
#    "attrs" : attrs_df,
#    "middle" : middle_df,
#    "att" : att_df
}

#gui = show(octs_df)
gui = show(octs_df, wsums_df, middle_df, att_df, dm_df, cd_df, fb_df, wm_df, amc_df, amlr_df)