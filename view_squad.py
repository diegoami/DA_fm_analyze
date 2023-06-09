import dash
from dash import html
from dash import dcc
import argparse
import yaml
from fmanalyze.aggregate.collect import create_full_squad_dfs
import os
from dash.dependencies import Input, Output, State
from fmanalyze.roles.formation import read_formation_for_select
from fmanalyze.ui.dash_helper import fill_style_conditions, create_fm_data_table, create_formation_layout
from dash.dependencies import Input, Output
import dash_html_components as html
from flask import Flask, render_template


config = None
server = Flask(__name__)


app_squads = dash.Dash(__name__, server=server, url_base_pathname='/squads/')
app_config = dash.Dash(__name__, server=server, url_base_pathname='/config/')


own_all_dfs = {}
color_dfs = {}
tab_dfs = {"OCTAGON" : ['octs', 'gk_octs'],
           "ATTRIBUTES" : ['tec', 'men', 'phys', 'goalk'],
           "ABILITIES" : ['tecabi', 'menabi', 'physabi']}

@server.route('/')
def index():
    return render_template('squad_index.html')

@app_config.callback(
    Output('redirect', 'pathname'),
    [Input('submit-button', 'n_clicks')],
    [State('role-dropdown', 'value')]
)
def on_button_click(n_clicks, value):
    if int(n_clicks) > 0:  # Cast n_clicks to an integer
        reload(value)
        return '/squads'
    return dash.no_update


@app_squads.callback(Output('tab-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    table_names = tab_dfs[tab]
    color_tables = [color_dfs[f'{table_name}_color'].drop(columns=['UID']) for table_name in table_names]
    df_tables = [own_all_dfs[table_name].drop(columns=['UID']) for table_name in table_names]
    style_condition_tables = [fill_style_conditions(color_table) for color_table in color_tables]
    # Set a fixed width for each column in pixels


    # Create the DataTable for df
    table_dfs = [create_fm_data_table(df_table, style_condition_table) for df_table, style_condition_table in zip(df_tables, style_condition_tables)]

    return html.Div([
        html.H4('Own Data'),
        html.Div([
            *table_dfs
        ], className='tables-container')
    ])





def reload(value = None):
    basedir, teamname, rivalname = config["basedir"], config["team"], config.get("rival", None)
    teamdir = os.path.join(basedir, 'teams', teamname)
    quantilesdir = os.path.join(basedir, 'quantiles')
    formation = config.get("formation", None)
    create_full_squad_dfs(teamdir, quantilesdir, own_all_dfs, color_dfs, formation=None, selected_role=value)
    # Define the layout of the app
    app_squads.layout = create_formation_layout(tab_dfs, 'OCTAGON')




def create_config_layout():
    basedir, teamname, rivalname = config["basedir"], config["team"], config.get("rival", None)
    teamdir = os.path.join(basedir, 'teams', teamname)

    team_dict = read_formation_for_select(teamdir, 'full_squad.csv')
    columns = create_role_columns()
    return html.Div([
        html.H1('Config'),
        html.Div(columns, className='row'),
        html.Button('Submit', id='submit-button', n_clicks=0),
        dcc.Location(id='redirect', refresh=True)
    ])


def create_role_columns():
    columns = []
    columns.append(html.Div([
            html.Label(f'Role '),
            dcc.Dropdown(
                id=f'role-dropdown',
                options=[{'label': value, 'value': value} for value in
                         ['GK', 'DR', 'DC', 'DL', 'WBR', 'DM', 'WBL', 'MR', 'MC', 'ML', 'AMR', 'AMC', 'AML', 'STC']]
            ),
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