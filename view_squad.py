import dash
from dash import html
from dash import dcc
import argparse
import yaml

from fmanalyze.aggregate.collect import create_formation_dfs
import os
from dash.dependencies import Input, Output
import dash_html_components as html

from fmanalyze.ui.dash_helper import fill_style_conditions, create_fm_data_table

app = dash.Dash(__name__)
own_all_dfs = {}
rival_all_dfs = {}
color_dfs = {}
rival_color_dfs = {}

@app.callback(Output('tab-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    color_df = color_dfs[f'{tab}_color']
    df = own_all_dfs[tab]
    style_conditions = fill_style_conditions(color_df)
    # Set a fixed width for each column in pixels


    # Create the DataTable for df
    table_df = create_fm_data_table(df, style_conditions)


    if rival_all_dfs:
        rival_df = rival_all_dfs[tab]
        rival_color_df = rival_color_dfs[f'{tab}_color']
        rival_style_conditions = fill_style_conditions(rival_color_df)

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help="required argument --config <config>")
    args = parser.parse_args()

    with open(args.config, 'r') as confhandle:
        config = yaml.safe_load(confhandle)

    basedir, teamname, rivalname = config["basedir"], config["team"], config.get("rival", None)
    teamdir, rivaldir = os.path.join(basedir, 'teams', teamname), os.path.join(basedir, 'teams',
                                                                               rivalname) if rivalname else None
    quantilesdir = os.path.join(basedir, 'quantiles')
    formation, rivalformation = config.get("formation", None), config.get("rivalformation", None)

    league_dir = os.path.dirname(basedir)

    create_formation_dfs(teamdir, rivaldir, quantilesdir, formation, rivalformation,
                         own_all_dfs, color_dfs, rival_all_dfs, rival_color_dfs)

    # Define the layout of the app
    app.layout = html.Div([
        dcc.Tabs(id='tabs', value='octs', children=[
            dcc.Tab(label=name, value=name) for name in own_all_dfs.keys()
        ]),
        html.Div(id='tab-content')
    ])

    app.run_server(debug=True)