import dash
from dash import html
from dash import dcc
import dash_table
import pandas as pd
import argparse
import yaml

from fmanalyze.aggregate.collect import fill_all_dfs
from fmanalyze.aggregate.color import create_color_roles_dfs, fill_color_dfs
import os
from dash.dependencies import Input, Output
import dash_html_components as html

app = dash.Dash(__name__)
own_all_dfs = {}
rival_all_dfs = {}
color_dfs = {}

color_map = {-2: 'red', -1: 'orange', 0: 'yellow', 1: 'lightgreen', 2: 'darkgreen'}
@app.callback(Output('tab-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    color_df = color_dfs[f'{tab}_color']

    df = own_all_dfs[tab]
    rival_df = rival_all_dfs[tab]

    style_conditions = fill_style_conditions(color_df)

    # Create the DataTable for df
    table_df = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_data_conditional=style_conditions
    )

    # Create the DataTable for rival_df
    table_rival_df = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in rival_df.columns],
        data=rival_df.to_dict('records'),
        style_data_conditional=style_conditions
    )

    # Return a Div containing both DataTables
    return html.Div([
        html.H4('Own Data'),
        table_df,
        html.H4('Rival Data'),
        table_rival_df
    ])

def fill_style_conditions(color_df):
    style_conditions = []
    for index, row in color_df.iterrows():
        for icol, col in enumerate(color_df.columns):
            if col not in ['Player', 'UID', 'Position']:
                content = row[col]
                style_conditions.append({
                    'if': {'row_index': index, 'column_id': col},
                    'backgroundColor': color_map[content],
                })
    return style_conditions


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
    rivaldir = config.get("rivaldir", None)
    formation_flag = config["formation"]
    # league dir is the parent directory of basedir
    league_dir = os.path.dirname(basedir)
    formation_df, formation_rivalo_df = None, None
    #all_csvs = ['octs', 'gk_octs']
    if formation_flag:
        formation_df = pd.read_csv(f'{basedir}/formation.csv')
        if rivaldir is not None:
            formation_rival_df = pd.read_csv(f'{rivaldir}/formation.csv')
    color_roles_dfs = create_color_roles_dfs(league_dir)

    fill_all_dfs(own_all_dfs, basedir, formation_df)
    fill_color_dfs(color_dfs, own_all_dfs, color_roles_dfs)
    if rivaldir is not None:
        fill_all_dfs(rival_all_dfs, rivaldir, formation_rival_df)
        fill_color_dfs(color_dfs, rival_all_dfs, color_roles_dfs)

    # Define the layout of the app
    app.layout = html.Div([
        dcc.Tabs(id='tabs', value='octs', children=[
            dcc.Tab(label=name, value=name) for name in own_all_dfs.keys()
        ]),
        html.Div(id='tab-content')
    ])

    app.run_server(debug=True)