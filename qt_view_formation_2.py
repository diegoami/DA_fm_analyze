import argparse
import yaml
import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                             QWidget, QLabel, QComboBox, QPushButton, QSizePolicy, QSplitter, QToolBar,
                             QMenuBar, QAction)

from fmanalyze.roles.formation import (read_formation_for_select, read_formation,
                                       convert_formation_to_dict, create_formation_df)
from fmanalyze.aggregate.collect import create_formation_dfs, read_formations
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import Qt
from fmanalyze.ui.qt_helper import (create_formation_layout)

config = None


own_all_dfs = {}
rival_all_dfs = {}
color_dfs = {}
rival_color_dfs = {}
tab_dfs = {"OCTAGON" : ['octs', 'gk_octs'],
           "ATTRIBUTES" : ['tec', 'men', 'phys', 'goalk'],
           "ABILITIES" : ['tecabi', 'menabi', 'physabi']}


class DashToPyQtApp(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.tabs = None
        self.rivaltabs = None
        self.config = config
        self.basedir, self.teamname = config["basedir"], config["team"]
        self.teamdir = os.path.join(self.basedir, 'teams', self.teamname)
        self.rivalname = config["rival"]
        self.rivaldir = os.path.join(self.basedir, 'teams', self.rivalname)
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

        # Create menubar
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)
        view_menu = menubar.addMenu("View")

        # Create toolbar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Create actions for menubar and toolbar
        toggle_combobox_panel_action = QAction("Toggle Combobox Panel", self)
        toggle_combobox_panel_action.triggered.connect(self.toggle_combobox_panel)
        view_menu.addAction(toggle_combobox_panel_action)
        toolbar.addAction(toggle_combobox_panel_action)

        self.splitter = QSplitter(Qt.Vertical)  # Create a vertical splitter
        self.main_layout.addWidget(self.splitter)


    def update_player_combobox(self, combobox_dir):
        role_combobox = self.sender()
        player_combobox = role_combobox.property("associatedPlayerCombobox")

        selected_role = role_combobox.currentText()
        new_players_data = read_formation(combobox_dir, full_squad=True, selected_role=selected_role)
        new_players = convert_formation_to_dict(new_players_data)
        player_combobox.clear()
        for uid, player in new_players.items():
            player_combobox.addItem(player, uid)

    def on_own_role_combobox_changed(self):
        self.update_player_combobox(self.teamdir)

    def on_rival_role_combobox_changed(self):
        self.update_player_combobox(self.rivaldir)

    def create_combobox_panel(self, config):
        combobox_panel = QWidget()
        combobox_layout = QVBoxLayout(combobox_panel)

        team_columns = self.create_player_columns('own')
        rival_columns = self.create_player_columns('rival')

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

        team_grid_layout.addWidget(self.create_files_widget(), 3, 2)
        # Add rival columns to the rival grid layout
        for i, column in enumerate(rival_columns):
            column_widget = QWidget()
            column_widget.setLayout(column)
            rival_grid_layout.addWidget(column_widget, i // grid_columns, i % grid_columns)
        team_grid_layout.addWidget(self.create_files_widget(), 3, 2)

        # Add grid layouts to the main layout
        combobox_layout.addWidget(QLabel('Config'))
        combobox_layout.addLayout(team_grid_layout)

        combobox_layout.addWidget(QLabel('Rival Config'))
        combobox_layout.addLayout(rival_grid_layout)

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.on_submit_button_clicked)
        combobox_layout.addWidget(submit_button)

        return combobox_panel

    def on_load_button_clicked(self):
        pass

    def on_save_button_clicked(self):
        pass

    def create_files_widget(self, which_one='own'):
        files_widget = QWidget()
        column_layout = QVBoxLayout()
        load_button = QPushButton('Load')
        load_button.clicked.connect(self.on_load_button_clicked)
        save_button = QPushButton('Save')
        load_button.clicked.connect(self.on_save_button_clicked)

        column_layout.addWidget(load_button)
        column_layout.addWidget(save_button)
        files_widget.setLayout(column_layout)
        return files_widget

    def create_player_columns(self, prefix='own'):

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
        quantilesdir = os.path.join(self.basedir, 'quantiles')
        load_formation, load_rival_formation = config.get("load_formation", None), config.get("load_rival_formation",
                                                                                              None)
        save_formation, save_rival_formation = config.get("save_formation", 'formation_current.csv'), config.get(
            'save_rival_formation', 'formation_current.csv')
        if own_formation is not None and rival_formation is not None:
            formation_df, formation_rival_df = own_formation, rival_formation
            own_formation.to_csv(os.path.join(self.teamdir, save_formation), index=False)
            rival_formation.to_csv(os.path.join(self.rivaldir, save_rival_formation), index=False)
        else:
            formation_df, formation_rival_df = read_formations(self.teamdir, load_formation, self.rivaldir, load_rival_formation)

        create_formation_dfs(self.teamdir, self.rivaldir, quantilesdir, formation_df, formation_rival_df,
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


        self.tabs, self.rivaltabs = create_formation_layout(tab_dfs, 'OCTAGON', color_dfs, own_all_dfs, rival_all_dfs, rival_color_dfs)

        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set the size policy to Expanding
        self.rivaltabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set the size policy to Expanding

        if self.rivaltabs:
            self.splitter.insertWidget(0, self.rivaltabs)
        if self.tabs:
            self.splitter.insertWidget(0, self.tabs)

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
