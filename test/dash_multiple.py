import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_table

app = dash.Dash(__name__)

# Sample DataFrame
data = {"Category": ["Category1", "Category2", "Category3"]}
df = pd.DataFrame(data)

# Create options for the combobox using DataFrame column data
data_options = [{"label": category, "value": category} for category in df["Category"]]

# Define the layout of the app
app.layout = html.Div([
    html.H2("Select Categories"),
    html.Div([
        dcc.Dropdown(id="combo1", options=data_options),
        dcc.Dropdown(id="combo2", options=data_options),
        html.Button("Submit", id="submit-button"),
    ]),
    html.Hr(),
    dcc.Tabs(id="tabs"),
])

@app.callback(
    Output("tabs", "children"),
    [Input("submit-button", "n_clicks")],
    [State("combo1", "value"), State("combo2", "value")],
)
def generate_tabs(n_clicks, *args):
    if n_clicks is None:
        return []

    # Access the selected values
    combo1_val, combo2_val = args

    # Generate DataFrames based on the selected options
    data = {"Column1": [1, 2, 3], "Column2": [4, 5, 6], "Column3": [7, 8, 9]}
    df1 = pd.DataFrame(data)
    df2 = df1 * 2

    # Create a list of tables to display in separate tabs
    tables = []
    for i, df in enumerate([df1, df2]):
        table = dash_table.DataTable(
            id=f"table-{i}",
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict("records"),
        )
        tables.append(dcc.Tab(label=f"Table {i+1}", value=f"tab-{i}", children=[table]))

    return tables

if __name__ == "__main__":
    app.run_server(debug=True)
