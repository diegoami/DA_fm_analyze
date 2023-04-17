import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1('Form Example'),
    html.Div([
        html.Label('Combobox 1'),
        dcc.Dropdown(
            id='combobox-1',
            options=[{'label': 'Option 1', 'value': 'option-1'},
                     {'label': 'Option 2', 'value': 'option-2'},
                     {'label': 'Option 3', 'value': 'option-3'}],
            value='option-1'
        ),
        html.Label('Combobox 2'),
        dcc.Dropdown(
            id='combobox-2',
            options=[{'label': 'Option A', 'value': 'option-a'},
                     {'label': 'Option B', 'value': 'option-b'},
                     {'label': 'Option C', 'value': 'option-c'}],
            value='option-a'
        ),
        html.Button('Submit', id='submit-button', n_clicks=0)
    ]),
    html.Div(id='tabs-content')
])

@app.callback(
    dash.dependencies.Output('tabs-content', 'children'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('combobox-1', 'value'),
     dash.dependencies.State('combobox-2', 'value')])
def update_output(n_clicks, combobox_1_value, combobox_2_value):
    if n_clicks > 0:
        # Generate the dataframes based on the input from the form
        df_1 = pd.DataFrame({'Column 1': [combobox_1_value, combobox_1_value],
                             'Column 2': [combobox_2_value, combobox_2_value]})
        df_2 = pd.DataFrame({'Column A': [combobox_1_value, combobox_1_value],
                             'Column B': [combobox_2_value, combobox_2_value]})

        # Create a dcc.Tab component for each dataframe
        tabs = [dcc.Tab(label='Dataframe 1', children=[
                        dcc.Graph(figure={
                            'data': [{
                                'x': df_1['Column 1'],
                                'y': df_1['Column 2'],
                                'type': 'bar'
                            }]
                        })
                    ]),
                dcc.Tab(label='Dataframe 2', children=[
                    dcc.Graph(figure={
                        'data': [{
                            'x': df_2['Column A'],
                            'y': df_2['Column B'],
                            'type': 'scatter'
                        }]
                    })
                ])]

        # Return the list of dcc.Tab components as the children of the dcc.Tabs component
        return dcc.Tabs(children=tabs)

if __name__ == '__main__':
    app.run_server(debug=True)
