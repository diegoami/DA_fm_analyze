import dash_table

color_map = {-2: 'red', -1: 'orange', 0: 'yellow', 1: 'lightgreen', 2: 'darkgreen'}

def fill_style_conditions(color_df, tab):
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


def create_fm_data_table(df, style_conditions):
    column_width = 150

    # Modify the style_cell in both DataTables
    style_cell = {
        'textAlign': 'center',
        'minWidth': f'{column_width}px',
        'maxWidth': f'{column_width}px',
        'width': f'{column_width}px',
        'padding': '8px',
        'border': '1px solid #ddd',
        'font-family': 'Arial, sans-serif'
    }

    # Modify the style_header in both DataTables
    style_header = {
        'textAlign': 'center',
        'backgroundColor': '#f2f2f2',
        'fontWeight': 'bold',
        'padding': '8px',
        'border': '1px solid #ddd',
        'font-family': 'Arial, sans-serif'
    }

    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_data_conditional=style_conditions,
        style_cell=style_cell,
        style_header=style_header
    )
