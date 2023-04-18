import dash
from dash import html
from dash import dcc
import dash_table
import pandas as pd
import argparse
from pandasgui import show
import pandas
import yaml
from fmanalyze.selection import formation
from fmanalyze.attrs.main_attrs import separate_in_tec_men_phys
from fmanalyze.attrs.abilities import split_abilities
from fmanalyze.roles.extract import COL_ROLES
import os
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
all_dfs = {}


@app.callback(Output('tab-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    df = all_dfs[tab]
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],  # Add column id
        data=df.to_dict('records')
    )

if __name__ == '__main__':
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
    formation_flag = config["formation"]
    all_csvs = ['octs', 'gk_octs']
    if formation_flag:
        formation_df = pd.read_csv(f'{basedir}/formation.csv')
    else:
        formation_df = None

    for csv in all_csvs:
        csv_df = pandas.read_csv(f'{basedir}/{csv}.csv')
        if formation_df is not None:
            csv_df = formation_df.merge(csv_df, on='UID', how='inner').drop(columns=['Player_y']).rename(columns={'Player_x': 'Player'})
        all_dfs[csv] = csv_df

    all_attrs = pandas.read_csv(f'{basedir}/all_attrs.csv')
    all_abilities = pandas.read_csv(f'{basedir}/abis.csv')

    if formation_df is not None:
        all_attrs = formation_df.merge(all_attrs, on='UID', how='inner').drop(columns=['Player_y']).rename(columns={'Player_x': 'Player'})
        all_abilities = formation_df.merge(all_abilities, on='UID', how='inner').drop(columns=['Player_y']).rename(columns={'Player_x': 'Player'})

    all_dfs['tec'], all_dfs['men'], all_dfs['phys'] = separate_in_tec_men_phys(all_attrs)

    all_dfs['tecabi'], all_dfs['menabi'], all_dfs['physabi'] = split_abilities(all_abilities)

    # league dir is the parent directory of basedir
    league_dir = os.path.dirname(basedir)

    color_dfs = {f'{name}_color': df.copy() for name, df in all_dfs.items()}
    for name, df in color_dfs.items():
        df.loc[:, ~df.columns.isin(["Player", "UID"])] = 0

    color_roles_dfs = {}
    for role in COL_ROLES:
        quantile_abi_df_name, quantile_attr_df_name, quantile_octs_df_name = f'quantiles_{role}_abis', f'quantiles_{role}_attrs', f'quantiles_{role}_octs'
        color_roles_dfs[quantile_abi_df_name] = pd.read_csv(f'{league_dir}/{quantile_abi_df_name}.csv')
        color_roles_dfs[quantile_attr_df_name] = pd.read_csv(f'{league_dir}/{quantile_attr_df_name}.csv')
        color_roles_dfs[quantile_octs_df_name] = pd.read_csv(f'{league_dir}/{quantile_octs_df_name}.csv')

    for name, df in all_dfs.items():
        if name in ['tec', 'men', 'phys']:
            print("Processing", name)
            for item, row in df.iterrows():
                player, uid = row['Player'], row['UID']
                position = row['Position']
                if name in ['tec', 'men', 'phys']:
                    ref_color_df = color_roles_dfs[f'quantiles_{position}_attrs']
                    color_df = color_dfs[f'{name}_color']

                    for index, ref_color_row in ref_color_df.iterrows():

                        col = ref_color_row['COL']
                        if col in df.columns:
                            if row[col] < ref_color_row['Q20']:
                                color_df.loc[(color_df['UID'] == uid), col] = -2
                            if row[col] >= ref_color_row['Q20'] and row[col] < ref_color_row['Q40']:
                                color_df.loc[(color_df['UID'] == uid), col] = -1
                            elif row[col] >= ref_color_row['Q40'] and row[col] < ref_color_row['Q60']:
                                color_df.loc[(color_df['UID'] == uid), col] = 0
                            elif row[col] >= ref_color_row['Q60'] and row[col] < ref_color_row['Q80']:
                                color_df.loc[(color_df['UID'] == uid), col] = 1
                            elif row[col] >= ref_color_row['Q80']:
                                color_df.loc[(color_df['UID'] == uid), col] = 2
    # Initialize the Dash app
   # app = dash.Dash(__name__)

    # Define the layout of the app
    app.layout = html.Div([
        dcc.Tabs(id='tabs', value='octs', children=[
            dcc.Tab(label=name, value=name) for name in all_dfs.keys()
        ]),
        html.Div(id='tab-content')
    ])

    app.run_server(debug=True)