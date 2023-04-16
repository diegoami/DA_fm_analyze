import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QTabWidget
from PyQt5.QtGui import QColor

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

    for i, column in enumerate(df.columns):
        for j, value in enumerate(df[column]):
            item = QTableWidgetItem(str(value))
            if column == 'value':
                item.setBackground(color_based_on_distribution(df[column])[j])
            table.setItem(j, i, item)

    table.setHorizontalHeaderLabels(df.columns)
    return table

# Create a PyQt5 application with tabs for each DataFrame
app = QApplication(sys.argv)

window = QWidget()
layout = QVBoxLayout(window)

tab_widget = QTabWidget()

for name, df in dataframes.items():
    table_widget = create_table_widget(df)
    tab_widget.addTab(table_widget, name)

layout.addWidget(tab_widget)
window.show()

sys.exit(app.exec_())
