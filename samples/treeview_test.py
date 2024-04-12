import tkinter as tk
from tkinter import ttk

# def on_edit(event):
#     item = tree.focus()
#     column = tree.identify_column(event.x)
#     tree.item(item, values=(input("Enter new value: "),))

def on_edit(event):
    columns=("column1", "column2")
    item = tree.focus()
    values = []
    for col in columns:
        new_value = input(f"Enter new value for {col}: ")
        values.append(new_value)
    tree.item(item, values=values)

# Create the tkinter window
root = tk.Tk()
root.title("Editable TreeView")

# Create a Treeview widget
tree = ttk.Treeview(root, columns=("column1", "column2"), show="headings")
tree.heading("#1", text="Column 1")
tree.heading("#2", text="Column 2")
tree.pack()

# Sample data list
data_list = [("row1_value1", "row1_value2"), ("row2_value1", "row2_value2")]

# Insert data from the list into the treeview
for item in data_list:
    tree.insert("", "end", values=item)

# Bind the on_edit function to the treeview
tree.bind("<Double-1>", on_edit)

# Run the tkinter main loop
root.mainloop()