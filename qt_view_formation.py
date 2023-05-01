import argparse
import yaml
from fmanalyze.roles.formation import read_formation_for_select, read_selected_formation, read_formation, \
    convert_formation_to_dict
import sys

from fmanalyze.aggregate.collect import create_formation_dfs, read_formations
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QLabel, QComboBox, QPushButton, QHBoxLayout, QSizePolicy, QSplitter
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import pandas as pd

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


def create_formation_layout(dfs, value):
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

config = None


own_all_dfs = {}
rival_all_dfs = {}
color_dfs = {}
rival_color_dfs = {}
tab_dfs = {"OCTAGON" : ['octs', 'gk_octs'],
           "ATTRIBUTES" : ['tec', 'men', 'phys', 'goalk'],
           "ABILITIES" : ['tecabi', 'menabi', 'physabi']}



def create_formation_df(positions, uids):
    df = pd.DataFrame(columns=['Position', 'UID'])
    df['Position'] = positions
    df['UID'] = uids
    df.dropna(inplace=True)
    df['UID'] = df['UID'].astype('int64')
    return df


class DashToPyQtApp(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.tabs = None
        self.rivaltabs = None
        self.config = config
        self.title = "Dash to PyQt App"
        self.init_ui()
        self.reload(config)
        self.init_comboboxes(config)

        self.splitter.setSizes([400, 400, 200])

    def toggle_combobox_panel(self):
        combobox_panel = self.splitter.widget(2)  # Assuming the combobox panel is at index 2
        combobox_panel.setVisible(not combobox_panel.isVisible())
    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 1200, 800)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.main_layout = QVBoxLayout(self.main_widget)
        self.toggle_combobox_panel_button = QPushButton("Toggle Combobox Panel")
        self.toggle_combobox_panel_button.clicked.connect(self.toggle_combobox_panel)
        self.main_layout.addWidget(self.toggle_combobox_panel_button)


        self.splitter = QSplitter(Qt.Vertical)  # Create a vertical splitter
        self.main_layout.addWidget(self.splitter)

    def on_own_role_combobox_changed(self, index):
        config = self.config
        basedir, teamname, rivalname = config["basedir"], config["team"], config.get("rival", None)
        teamdir, rivaldir = os.path.join(basedir, 'teams', teamname), os.path.join(basedir, 'teams',
                                                                                   rivalname) if rivalname else None

        role_combobox = self.sender()
        player_combobox = role_combobox.property("associatedPlayerCombobox")

        selected_role = role_combobox.currentText()
        new_players_data = read_formation(teamdir, full_squad=True, selected_role=selected_role)
        new_players = convert_formation_to_dict(new_players_data)
        player_combobox.clear()
        for uid, player in new_players.items():
            player_combobox.addItem(player, uid)

    def on_rival_role_combobox_changed(self, index):
        config = self.config
        basedir, teamname, rivalname = config["basedir"], config["team"], config.get("rival", None)
        teamdir, rivaldir = os.path.join(basedir, 'teams', teamname), os.path.join(basedir, 'teams',
                                                                                   rivalname) if rivalname else None

        role_combobox = self.sender()
        player_combobox = role_combobox.property("associatedPlayerCombobox")

        selected_role = role_combobox.currentText()
        new_players_data = read_formation(rivaldir, full_squad=True, selected_role=selected_role)
        new_players = convert_formation_to_dict(new_players_data)
        player_combobox.clear()
        for uid, player in new_players.items():
            player_combobox.addItem(player, uid)


    def create_combobox_panel(self, config):
        combobox_panel = QWidget()
        combobox_layout = QVBoxLayout(combobox_panel)
        basedir, teamname, rivalname = config["basedir"], config["team"], config.get("rival", None)
        teamdir, rivaldir = os.path.join(basedir, 'teams', teamname), os.path.join(basedir, 'teams',
                                                                                   rivalname) if rivalname else None

        load_formation, load_rival_formation = config.get("load_formation", None), config.get("load_rival_formation",
                                                                                              None)
        save_formation, save_rival_formation = config.get("save_formation", None), config.get("save_rival_formation",
                                                                                              None)

        team_dict = read_formation_for_select(teamdir, 'full_squad.csv')
        rival_dict = read_formation_for_select(rivaldir, 'full_squad.csv')

        team_columns = self.create_player_columns(team_dict, 'own')
        rival_columns = self.create_player_columns(rival_dict, 'rival')

        # Create grid layouts for team and rival comboboxes
        team_grid_layout = QGridLayout()
        rival_grid_layout = QGridLayout()

        # Define the number of rows and columns for the grid
        grid_rows = 4
        grid_columns = (len(team_columns) + grid_rows - 1) // grid_rows

        # Add team columns to the team grid layout
        for i, column in enumerate(team_columns):
            column_widget = QWidget()
            column_widget.setLayout(column)
            team_grid_layout.addWidget(column_widget, i // grid_columns, i % grid_columns)

        # Add rival columns to the rival grid layout
        for i, column in enumerate(rival_columns):
            column_widget = QWidget()
            column_widget.setLayout(column)
            rival_grid_layout.addWidget(column_widget, i // grid_columns, i % grid_columns)

        # Add grid layouts to the main layout
        combobox_layout.addWidget(QLabel('Config'))
        combobox_layout.addWidget(QLabel(f'Loaded from {load_formation}, saving to {save_formation}'))
        combobox_layout.addLayout(team_grid_layout)

        combobox_layout.addWidget(QLabel('Rival Config'))
        combobox_layout.addWidget(QLabel(f'Loaded from {load_rival_formation}, saving to {save_rival_formation}'))
        combobox_layout.addLayout(rival_grid_layout)

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.on_submit_button_clicked)
        combobox_layout.addWidget(submit_button)

        return combobox_panel
    def create_player_columns(self, team_dict, prefix='own'):

        columns = []
        for index in range(1, 12):
            column_layout = QVBoxLayout()

            role_label = QLabel(f'Role {index}')
            column_layout.addWidget(role_label)

            role_combobox = QComboBox()
            role_combobox.setObjectName(f'{prefix}-role{index}-dropdown')
            role_combobox.addItems(
                ['GK', 'DR', 'DC', 'DL', 'WBR', 'DM', 'WBL', 'MR', 'MC', 'ML', 'AMR', 'AMC', 'AML', 'STC'])
            role_combobox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Set the size policy to fixed
            role_combobox.setCurrentIndex(-1)
            column_layout.addWidget(role_combobox)

            player_label = QLabel(f'Player {index}')
            column_layout.addWidget(player_label)

            player_combobox = QComboBox()
            player_combobox.setObjectName(f'{prefix}-player{index}-dropdown')
            #for uid, player in team_dict.items():
            #    player_combobox.addItem(player, uid)
            player_combobox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Set the size policy to fixed
            player_combobox.setMinimumWidth(150)
            column_layout.addWidget(player_combobox)
            if prefix == 'own':
                role_combobox.currentIndexChanged.connect(self.on_own_role_combobox_changed)
            else:
                role_combobox.currentIndexChanged.connect(self.on_rival_role_combobox_changed)
            role_combobox.setProperty("associatedPlayerCombobox", player_combobox)
            columns.append(column_layout)
        return columns

    def reload(self, config, own_formation=None, rival_formation=None):
        basedir, teamname, rivalname = config["basedir"], config["team"], config.get("rival", None)
        teamdir, rivaldir = os.path.join(basedir, 'teams', teamname), os.path.join(basedir, 'teams',
                                                                                   rivalname) if rivalname else None
        quantilesdir = os.path.join(basedir, 'quantiles')
        load_formation, load_rival_formation = config.get("load_formation", None), config.get("load_rival_formation",
                                                                                              None)
        save_formation, save_rival_formation = config.get("save_formation", 'formation_current.csv'), config.get(
            'save_rival_formation', 'formation_current.csv')
        if own_formation is not None and rival_formation is not None:
            formation_df, formation_rival_df = own_formation, rival_formation
            own_formation.to_csv(os.path.join(teamdir, save_formation), index=False)
            rival_formation.to_csv(os.path.join(rivaldir, save_rival_formation), index=False)
        else:
            formation_df, formation_rival_df = read_formations(teamdir, load_formation, rivaldir, load_rival_formation)

        create_formation_dfs(teamdir, rivaldir, quantilesdir, formation_df, formation_rival_df,
                             own_all_dfs, color_dfs, rival_all_dfs, rival_color_dfs)
        # Define the layout of the app
        if self.tabs:
            self.main_layout.removeWidget(self.tabs)
            self.tabs.deleteLater()
            self.tabs = None

        if self.rivaltabs:
            self.main_layout.removeWidget(self.rivaltabs)
            self.rivaltabs.deleteLater()
            self.rivaltabs = None


        self.tabs, self.rivaltabs = create_formation_layout(tab_dfs, 'OCTAGON')

        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set the size policy to Expanding
        self.rivaltabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set the size policy to Expanding

        self.tabs, self.rivaltabs = create_formation_layout(tab_dfs, 'OCTAGON')

        if self.tabs:
            self.splitter.addWidget(self.tabs)
        if self.rivaltabs:
            self.splitter.addWidget(self.rivaltabs)

    def init_comboboxes(self, config):
        combobox_panel = self.create_combobox_panel(config)
        self.splitter.addWidget(combobox_panel)  # Add the combobox panel to the splitter

    def on_submit_button_clicked(self):
        own_roles = []
        own_players = []
        rival_roles = []
        rival_players = []

        for index in range(1, 12):
            own_role_combobox = self.findChild(QComboBox, f'own-role{index}-dropdown')
            own_player_combobox = self.findChild(QComboBox, f'own-player{index}-dropdown')
            rival_role_combobox = self.findChild(QComboBox, f'rival-role{index}-dropdown')
            rival_player_combobox = self.findChild(QComboBox, f'rival-player{index}-dropdown')

            own_roles.append(own_role_combobox.currentText())
            own_players.append(own_player_combobox.currentData())
            rival_roles.append(rival_role_combobox.currentText())
            rival_players.append(rival_player_combobox.currentData())

        own_formation = create_formation_df(own_roles, own_players)
        rival_formation = create_formation_df(rival_roles, rival_players)

        own_formation.dropna(inplace=True)
        rival_formation.dropna(inplace=True)

        self.reload(self.config, own_formation, rival_formation)

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
