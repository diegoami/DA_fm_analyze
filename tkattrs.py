
import tkinter as tk
from tkinter import ttk
import pandas as pd
# Function to create table header
def create_header(parent, columns, row=0):
    for col, column_name in enumerate(columns):
        label = ttk.Label(parent, text=column_name, borderwidth=1, relief="solid")
        label.grid(row=row, column=col, sticky="nsew")

# Function to create table body
def create_body(parent, dataframe, row_start=1):
    for row, record in dataframe.iterrows():
        for col, value in enumerate(record):
            entry = ttk.Entry(parent)
            entry.insert(0, value)
            entry.config(state="readonly")
            entry.grid(row=row + row_start, column=col, sticky="nsew")

# Initialize the Tkinter application
app = tk.Tk()
app.title("DataFrame Viewer")

frame = ttk.Frame(app, padding="3")
frame.grid(row=0, column=0, sticky="nsew")
new_df = pd.read_csv('rsana/octs.txt')
# Create table header and body
create_header(frame, new_df.columns)
create_body(frame, new_df)

app.mainloop()
