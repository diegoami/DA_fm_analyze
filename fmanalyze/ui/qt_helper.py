from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QWidget, QLabel, QComboBox, QPushButton, QHBoxLayout, QSizePolicy, QSplitter, QToolBar,
                             QMenu, QMenuBar, QAction)

color_map = {-2: 'red', -1: 'orange', 0: 'yellow', 1: 'lightgreen', 2: 'darkgreen'}
def fill_style_conditions(color_df):
    style_conditions = []
    for index, row in color_df.iterrows():
        for icol, col in enumerate(color_df.columns):
            if col not in ['Player', 'UID', 'Position']:
                content = row[col]
                style_conditions.append({
                    'row_index': index,
                    'column_id': col,
                    'backgroundColor': color_map[content],
                })
    return style_conditions


def create_fm_data_table(df, style_conditions, column_width=30):
    table = QTableWidget(df.shape[0], df.shape[1])

    table.setHorizontalHeaderLabels(df.columns)
    table.setVerticalHeaderLabels(df.index.astype(str))

    for index, row in df.iterrows():
        for icol, col in enumerate(df.columns):
            item = QTableWidgetItem(str(row[col]))
            item.setTextAlignment(Qt.AlignCenter)

            for cond in style_conditions:
                if cond['row_index'] == index and cond['column_id'] == col:
                    item.setBackground(QColor(cond['backgroundColor']))

            table.setItem(index, icol, item)

    table.resizeColumnsToContents()
    return table


def create_formation_layout(dfs, value, color_dfs, own_all_dfs, rival_all_dfs, rival_color_dfs):
    tab_widget = QTabWidget()
    rival_tab_widget = QTabWidget()
    for tab_name, table_names in dfs.items():
        tab = QWidget()
        tab_layout = QHBoxLayout(tab)
        rival_tab = QWidget()
        rival_tab_layout = QHBoxLayout(rival_tab)
        for table_name in table_names:
            style_conditions = fill_style_conditions(color_dfs[f'{table_name}_color'].drop(columns=['UID']))
            table = create_fm_data_table(own_all_dfs[table_name].drop(columns=['UID']),style_conditions )
            tab_layout.addWidget(table)
            tab_widget.addTab(tab, tab_name)

            rival_style_conditions = fill_style_conditions(rival_color_dfs[f'{table_name}_color'].drop(columns=['UID']))
            rival_table = create_fm_data_table(rival_all_dfs[table_name].drop(columns=['UID']), rival_style_conditions)
            rival_tab_layout.addWidget(rival_table)
            rival_tab_widget.addTab(rival_tab, tab_name)


    return tab_widget, rival_tab_widget

