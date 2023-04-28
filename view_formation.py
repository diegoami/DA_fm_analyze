import dash
from dash import html
from dash import dcc
import argparse
import yaml
import pandas as pd
from fmanalyze.aggregate.collect import create_formation_dfs, read_formations
import os
from dash.dependencies import State
from fmanalyze.roles.formation import read_formation_for_select, read_selected_formation
from fmanalyze.ui.dash_helper import fill_style_conditions, create_fm_data_table, create_formation_layout
from dash.dependencies import Input, Output
import dash_html_components as html
from flask import Flask, render_template


config = None
# Create a Flask app
server = Flask(__name__)


app_formations = dash.Dash(__name__, server=server, url_base_pathname='/formations/')
app_config = dash.Dash(__name__, server=server, url_base_pathname='/config/')



own_all_dfs = {}
rival_all_dfs = {}
color_dfs = {}
rival_color_dfs = {}
tab_dfs = {"OCTAGON" : ['octs', 'gk_octs'],
           "ATTRIBUTES" : ['tec', 'men', 'phys', 'goalk'],
           "ABILITIES" : ['tecabi', 'menabi', 'physabi']}

@server.route('/')
def index():
    return render_template('formation_index.html')

num_comboboxes = 44
combobox_names = [f'own-role{index}-dropdown' for index in range(1,12)] + [f'own-player{index}-dropdown' for index in range(1,12)] + [f'rival-role{index}-dropdown' for index in range(1,12)] + [f'rival-player{index}-dropdown' for index in range(1,12)]

@app_config.callback(
    Output('redirect', 'href'),
    Output('redirect', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State(combobox_name, 'value') for combobox_name in combobox_names]
)
def on_button_click(n_clicks, *args):
    if int(n_clicks) > 0:  # Cast n_clicks to an integer

        own_formation = create_formation_df(args[:11], args[11:22])
        rival_formation = create_formation_df(args[22:33], args[33:])
        own_formation.dropna(inplace=True)
        rival_formation.dropna(inplace=True)
        reload(own_formation, rival_formation)
        return '/formations', 'Open Formations'
    return dash.no_update, dash.no_update


def create_formation_df(positions, uids):
    df = pd.DataFrame(columns=['Position', 'UID'])
    df['Position'] = positions
    df['UID'] = uids
    df.dropna(inplace=True)
    df['UID'] = df['UID'].astype('int64')
    return df

def process_formation():
    pass

@app_formations.callback(Output('tab-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    table_names = tab_dfs[tab]

    color_tables = [color_dfs[f'{table_name}_color'].drop(columns=['UID']) for table_name in table_names]
    df_tables = [own_all_dfs[table_name].drop(columns=['UID']) for table_name in table_names]
    style_condition_tables = [fill_style_conditions(color_table) for color_table in color_tables]
    # Set a fixed width for each column in pixels


    # Create the DataTable for df
    table_dfs = [create_fm_data_table(df_table, style_condition_table) for df_table, style_condition_table in zip(df_tables, style_condition_tables)]


    if rival_all_dfs:
        rival_df_tables = [rival_all_dfs[table_name].drop(columns=['UID']) for table_name in table_names]
        rival_color_tables =[rival_color_dfs[f'{table_name}_color'].drop(columns=['UID']) for table_name in table_names]
        rival_style_condition_tables = [fill_style_conditions(rival_color_table) for rival_color_table in rival_color_tables]

        table_rival_dfs = [create_fm_data_table(rival_df_table, rival_style_condition_table) for rival_df_table, rival_style_condition_table in zip(rival_df_tables, rival_style_condition_tables)]
        return html.Div([
            html.Div([
                html.H4('Own Data'),
                html.Div([
                    *table_dfs
                ], className='tables-container')
            ]),
            html.Div([
                html.H4('Rival Data'),
                html.Div([
                    *table_rival_dfs
                ], className='tables-container')
            ])
        ])
    else:
        return html.Div([
            html.H4('Own Data'),
            html.Div([
                *table_dfs
            ], className='tables-container')
        ])


def reload(own_formation = None, rival_formation = None):
    basedir, teamname, rivalname = config["basedir"], config["team"], config.get("rival", None)
    teamdir, rivaldir = os.path.join(basedir, 'teams', teamname), os.path.join(basedir, 'teams',
                                                                               rivalname) if rivalname else None
    quantilesdir = os.path.join(basedir, 'quantiles')
    load_formation, load_rival_formation = config.get("load_formation", None), config.get("load_rival_formation", None)
    save_formation, save_rival_formation = config.get("save_formation", 'formation_current.csv'), config.get('save_rival_formation', 'formation_current.csv')
    if own_formation is not None and rival_formation is not None:
        formation_df, formation_rival_df = own_formation, rival_formation
        own_formation.to_csv(os.path.join(teamdir, save_formation), index=False)
        rival_formation.to_csv(os.path.join(rivaldir, save_rival_formation), index=False)
    else:
        formation_df, formation_rival_df = read_formations(teamdir, load_formation, rivaldir, load_rival_formation)

    create_formation_dfs(teamdir, rivaldir, quantilesdir, formation_df, formation_rival_df,
                         own_all_dfs, color_dfs, rival_all_dfs, rival_color_dfs)
    # Define the layout of the app
    app_formations.layout = create_formation_layout(tab_dfs, 'OCTAGON')


def create_config_layout():
    basedir, teamname, rivalname = config["basedir"], config["team"], config.get("rival", None)
    teamdir, rivaldir = os.path.join(basedir, 'teams', teamname), os.path.join(basedir, 'teams',
                                                                               rivalname) if rivalname else None

    load_formation, load_rival_formation = config.get("load_formation", None), config.get("load_rival_formation", None)
    save_formation, save_rival_formation = config.get("save_formation", None), config.get("save_rival_formation", None)

    team_dict = read_formation_for_select(teamdir, 'full_squad.csv')
    rival_dict = read_formation_for_select(rivaldir, 'full_squad.csv')
    if load_formation:
        formation_lists = read_selected_formation(teamdir, load_formation)
    if load_rival_formation:
        rival_formation_lists = read_selected_formation(rivaldir, load_rival_formation)
    columns = create_player_columns(team_dict, 'own', formation_lists)
    rival_columns = create_player_columns(rival_dict, 'rival', rival_formation_lists)



    return html.Div([
        html.H1('Config'),
        html.H2(f'Loaded from {load_formation},  saving to  {save_formation}'),
        html.Div(columns, className='row'),
        html.H1('Rival Config'),
        html.H2(f'Loaded from {load_rival_formation}, saving to  {save_rival_formation}'),
        html.Div(rival_columns, className='row'),
        html.Button('Submit', id='submit-button', n_clicks=0),
        html.A('', id='redirect', target='_blank')
    ])


def create_player_columns(team_dict, prefix='own', formation_lists=None):
    if formation_lists:
        role_dropdowns_defaults, player_dropdowns_defaults = formation_lists
    columns = []
    for index in range(1, 12):
        columns.append(html.Div([
            html.Label(f'Role {index}'),
            dcc.Dropdown(
                id=f'{prefix}-role{index}-dropdown',
                options=[{'label': value, 'value': value} for value in
                         ['GK', 'DR', 'DC', 'DL', 'WBR', 'DM', 'WBL', 'MR', 'MC', 'ML', 'AMR', 'AMC', 'AML', 'STC']],
                          value=role_dropdowns_defaults[index - 1] if role_dropdowns_defaults else None
            ),
            html.Label(f'Player {index}'),
            dcc.Dropdown(
                id=f'{prefix}-player{index}-dropdown',
                options=[{'label': player, 'value': uid} for uid, player in team_dict.items()],
                value=player_dropdowns_defaults[index - 1] if player_dropdowns_defaults else None
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
    #app_formations.layout = create_formation_layout()

    server.run(debug=True)