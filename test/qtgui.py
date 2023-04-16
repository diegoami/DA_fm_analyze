import argparse
import pandas
import yaml
from fmanalyze.roles.extract import COL_ROLES
import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QTabWidget
from PyQt5.QtGui import QColor, QStandardItemModel


# Define a custom style function
def color_based_on_distribution(column):
    q1 = column.quantile(0.25)
    q2 = column.quantile(0.5)
    q3 = column.quantile(0.75)

    color_mapper = []

    for value in column:
        if value <= q1:
            color_mapper.append(QColor('red'))
        elif q1 < value <= q2:
            color_mapper.append(QColor('yellow'))
        elif q2 < value <= q3:
            color_mapper.append(QColor('lightgreen'))
        else:
            color_mapper.append(QColor('green'))

    return color_mapper

# Create a PyQt5 table widget from a pandas DataFrame with color-coded cells

def create_table_widget(df):
    table = QTableWidget()
    table.setRowCount(df.shape[0])
    table.setColumnCount(df.shape[1])
    table.setSortingEnabled(True)
    # Set a specific column to be pinned to the left
    #table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    for i, column in enumerate(df.columns):
        for j, value in enumerate(df[column]):
            item = QTableWidgetItem(str(value))
            # get type of columne
            if df[column].dtype == 'int64' or df[column].dtype == 'float64':
                item.setBackground(color_based_on_distribution(df[column])[j])
            table.setItem(j, i, item)

    table.setHorizontalHeaderLabels(df.columns)
    return table

# Create a PyQt5 application with tabs for each DataFrame


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

    app = QApplication(sys.argv)

    window = QWidget()
    layout = QVBoxLayout(window)
    tab_widget = QTabWidget()

    for name, df in all_dfs.items():
        model = QStandardItemModel()

        table_widget = create_table_widget(df)
        tab_widget.addTab(table_widget, name)

    layout.addWidget(tab_widget)
    window.show()

    sys.exit(app.exec_())
