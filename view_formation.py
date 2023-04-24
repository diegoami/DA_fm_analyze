import dash
from dash import html
from dash import dcc
import argparse
import yaml
import pandas as pd

from fmanalyze.aggregate.collect import create_formation_dfs
import os

from dash.dependencies import Input, Output, State

from fmanalyze.roles.formation import read_full_formation
from fmanalyze.ui.dash_helper import fill_style_conditions, create_fm_data_table
from dash.dependencies import Input, Output


import dash_html_components as html
from flask import Flask, render_template_string, render_template


config = None
# Create a Flask app
server = Flask(__name__)

# Define the index route

# Create the first Dash app


app_formations = dash.Dash(__name__, server=server, url_base_pathname='/formations/')
app_config = dash.Dash(__name__, server=server, url_base_pathname='/config/')



own_all_dfs = {}
rival_all_dfs = {}
color_dfs = {}
rival_color_dfs = {}

@server.route('/')
def index():
    return render_template('formation_index.html')



@app_config.callback(
    Output('redirect', 'pathname'),
    [Input('submit-button', 'n_clicks')]
)
def on_button_click(n_clicks):
    if int(n_clicks) > 0:  # Cast n_clicks to an integer
        return '/formations'
    return dash.no_update


@app_formations.callback(Output('tab-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    color_df = color_dfs[f'{tab}_color']
    df = own_all_dfs[tab]
    style_conditions = fill_style_conditions(color_df, tab)
    # Set a fixed width for each column in pixels


    # Create the DataTable for df
    table_df = create_fm_data_table(df, style_conditions)


    if rival_all_dfs:
        rival_df = rival_all_dfs[tab]
        rival_color_df = rival_color_dfs[f'{tab}_color']
        rival_style_conditions = fill_style_conditions(rival_color_df, tab)

        # Create the DataTable for rival_df
        table_rival_df = create_fm_data_table(rival_df, rival_style_conditions)
        return html.Div([
            html.Div([
                html.H4('Own Data'),
                table_df
            ]),
            html.Div([
                html.H4('Rival Data'),
                table_rival_df
            ])
        ])
    else:
        return html.Div([
            html.H4('Own Data'),
            table_df
        ])





def reload():
    basedir, teamname, rivalname = config["basedir"], config["team"], config.get("rival", None)
    teamdir, rivaldir = os.path.join(basedir, 'teams', teamname), os.path.join(basedir, 'teams',
                                                                               rivalname) if rivalname else None
    quantilesdir = os.path.join(basedir, 'quantiles')
    formation, rivalformation = config.get("formation", None), config.get("rivalformation", None)
    league_dir = os.path.dirname(basedir)
    create_formation_dfs(teamdir, rivaldir, quantilesdir, formation, rivalformation,
                         own_all_dfs, color_dfs, rival_all_dfs, rival_color_dfs)
    # Define the layout of the app
    app_formations.layout = html.Div([
        dcc.Tabs(id='tabs', value='octs', children=[
            dcc.Tab(label=name, value=name, className='custom-tab',
                    selected_className='custom-tab--selected') for name in own_all_dfs.keys()
        ]),
        html.Div(id='tab-content')
    ])




def create_config_layout():
    basedir, teamname, rivalname = config["basedir"], config["team"], config.get("rival", None)
    teamdir, rivaldir = os.path.join(basedir, 'teams', teamname), os.path.join(basedir, 'teams',
                                                                               rivalname) if rivalname else None

    team_dict = read_full_formation(teamdir, 'full_formation.csv')
    rival_dict = read_full_formation(rivaldir, 'full_formation.csv')
    columns = create_player_columns(team_dict, 'own')
    rival_columns = create_player_columns(rival_dict, 'rival')
    return html.Div([
        html.H1('Config'),
        html.Div(columns, className='row'),
        html.H1('Rival Config'),
        html.Div(rival_columns, className='row'),
        html.Button('Submit', id='submit-button', n_clicks=0),
        dcc.Location(id='redirect', refresh=True)
    ])


def create_player_columns(team_dict, prefix='own'):
    columns = []
    for index in range(1, 12):
        columns.append(html.Div([
            html.Label(f'Role {index}'),
            dcc.Dropdown(
                id=f'{prefix}-role{index}-dropdown',
                options=[{'label': value, 'value': value} for value in
                         ['GK', 'DR', 'DC', 'DL', 'WBR', 'DM', 'WBL', 'MR', 'MC', 'ML', 'AMR', 'AMC', 'AML', 'STC']]
            ),
            html.Label(f'Player {index}'),
            dcc.Dropdown(
                id=f'{prefix}-player{index}-dropdown',
                options=[{'label': player, 'value': uid} for uid, player in team_dict.items()]
            )

        ], className='sixcolumns'))
    return columns


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help="required argument --config <config>")
    args = parser.parse_args()

    with open(args.config, 'r') as confhandle:
        config = yaml.safe_load(confhandle)

    app_config.layout = create_config_layout()
    reload()

    server.run(debug=True)