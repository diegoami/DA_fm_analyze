import dash
from dash import html
from dash import dcc
import dash_table
import pandas as pd

# Create a sample DataFrame
data = {'Column1': [1, 2, 3],
        'Column2': [4, 5, 6],
        'Column3': [7, 8, 9]}
df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_data_conditional=[
            # Color the first cell in the first row
            {
                'if': {'row_index': 0, 'column_id': 'Column1'},
                'backgroundColor': 'red',
            },
            # Color the second cell in the second row
            {
                'if': {'row_index': 1, 'column_id': 'Column2'},
                'backgroundColor': 'blue',
            },
            # Color the third cell in the third row
            {
                'if': {'row_index': 2, 'column_id': 'Column3'},
                'backgroundColor': 'green',
            },
        ]
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
