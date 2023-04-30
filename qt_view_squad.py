import sys
import os
import argparse
import yaml
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from fmanalyze.aggregate.collect import create_full_squad_dfs

color_map = {-2: 'red', -1: 'orange', 0: 'yellow', 1: 'lightgreen', 2: 'darkgreen'}
own_all_dfs = {}
color_dfs = {}
tab_dfs = {"OCTAGON" : ['octs', 'gk_octs'],
           "ATTRIBUTES" : ['tec', 'men', 'phys', 'goalk'],
           "ABILITIES" : ['tecabi', 'menabi', 'physabi']}
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


def create_formation_layout(dfs, value):
    tab_widget = QTabWidget()

    for tab_name, table_names in dfs.items():
        tab = QWidget()
        tab_layout = QHBoxLayout(tab)

        for table_name in table_names:
            table = create_fm_data_table(own_all_dfs[table_name].drop(columns=['UID']), fill_style_conditions(color_dfs[f'{table_name}_color'].drop(columns=['UID'])))
            tab_layout.addWidget(table)

        tab_widget.addTab(tab, tab_name)

    return tab_widget


class DashToPyQtApp(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.tabs = None
        self.config = config
        self.title = "Dash to PyQt App"
        self.init_ui()
        self.reload()
        self.init_buttons()


    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 1200, 800)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.main_layout = QVBoxLayout(self.main_widget)


    def init_tabs(self):
        self.tabs = create_formation_layout(tab_dfs, 'OCTAGON')
        self.main_layout.addWidget(self.tabs)

    def init_buttons(self):
        self.button_layout = QHBoxLayout()

        self.role_label = QLabel("Role:")
        self.button_layout.addWidget(self.role_label)

        self.role_dropdown = QComboBox(self)
        for role in ['GK', 'DR', 'DC', 'DL', 'WBR', 'DM', 'WBL', 'MR', 'MC', 'ML', 'AMR', 'AMC', 'AML', 'STC']:
            self.role_dropdown.addItem(role)
        self.button_layout.addWidget(self.role_dropdown)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.on_submit_button_click)
        self.button_layout.addWidget(self.submit_button)

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.clicked.connect(self.on_reset_button_click)
        self.button_layout.addWidget(self.reset_button)

        self.main_layout.addLayout(self.button_layout)

    def on_submit_button_click(self):
        role_value = self.role_dropdown.currentText()
        self.reload(role_value)

    def on_reset_button_click(self):
        self.reload()

    def reload(self, value=None):
        basedir, teamname, rivalname = self.config["basedir"], self.config["team"], self.config.get("rival", None)
        teamdir = os.path.join(basedir, 'teams', teamname)
        quantilesdir = os.path.join(basedir, 'quantiles')
        formation = self.config.get("formation", None)
        create_full_squad_dfs(teamdir, quantilesdir, own_all_dfs, color_dfs, formation=formation, selected_role=value)
        # Remove the old tabs and create new ones
        if self.tabs:
            self.main_layout.removeWidget(self.tabs)
            self.tabs.deleteLater()
            self.tabs = None
        self.tabs = create_formation_layout(tab_dfs, 'OCTAGON')
        self.main_layout.insertWidget(0, self.tabs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help="required argument --config <config>")
    args = parser.parse_args()

    with open(args.config, 'r') as confhandle:
        config = yaml.safe_load(confhandle)

    app = QApplication(sys.argv)
    main_window = DashToPyQtApp(config)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
