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
        formation_df = formation.parse_selection(basedir)
    else:
        formation_df = None

    for csv in all_csvs:
        csv_df = pandas.read_csv(f'{basedir}/{csv}.csv')
        if formation_df is not None:
            csv_df = formation_df.merge(csv_df, on='UID', how='inner')
        all_dfs[csv] = csv_df

    all_attrs = pandas.read_csv(f'{basedir}/all_attrs.csv')
    all_dfs['tec'], all_dfs['men'], all_dfs['phys'] = separate_in_tec_men_phys(all_attrs)

    all_abilities = pandas.read_csv(f'{basedir}/abis.csv')
    all_dfs['tecabi'], all_dfs['menabi'], all_dfs['physabi'] = split_abilities(all_abilities)

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