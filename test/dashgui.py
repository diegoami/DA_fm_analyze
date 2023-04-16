import argparse
import pandas
import yaml
from fmanalyze.roles.extract import COL_ROLES
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

# Create sample DataFrames
data1 = {
    'category': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
    'value': [10, 20, 30, 40, 50, 60, 70, 80]
}
df1 = pd.DataFrame(data1)

data2 = {
    'category': ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'],
    'value': [15, 25, 35, 45, 55, 65, 75, 85]
}
df2 = pd.DataFrame(data2)

dataframes = {'DataFrame 1': df1, 'DataFrame 2': df2}

# Define a custom style function
def color_based_on_distribution(column):
    q1 = column.quantile(0.25)
    q2 = column.quantile(0.5)
    q3 = column.quantile(0.75)

    color_mapper = []

    for value in column:
        if value <= q1:
            color_mapper.append('red')
        elif q1 < value <= q2:
            color_mapper.append('yellow')
        elif q2 < value <= q3:
            color_mapper.append('lightgreen')
        else:
            color_mapper.append('green')

    return color_mapper

@app.callback(Output('tab-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    df = dataframes[tab]
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns if i != 'color'],
        data=df.to_dict('records'),
        style_data_conditional=[
            {
                'if': {
                    'column_id': 'value',
                    'row_index': i
                },
                'backgroundColor': df.loc[i, 'color']
            } for i in range(df.shape[0])
        ]
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--config')
    args = parser.parse_args()
    if args.config == None:
        print("required argument --config <config>")
        exit()
    else:
        with open(args.config, 'r') as confhandle:
            config = yaml.safe_load(confhandle)



    basedir = config["target_dir"]


    all_csvs = [f'{role}_attrs' for role in COL_ROLES]
    all_dfs = {}

    for csv in all_csvs:
        csv_df = pandas.read_csv(f'{basedir}/{csv}.csv')
        all_dfs[csv] = csv_df

    # Create a Dash app
    app = dash.Dash(__name__)

    app.layout = html.Div([
        dcc.Tabs(id='tabs', value='DataFrame 1', children=[
            dcc.Tab(label=name, value=name) for name in all_dfs.keys()
        ]),
        html.Div(id='tab-content')
    ])
