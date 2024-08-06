import tkinter as tk
from tkinter import ttk

def on_edit(event):
    # Get the item and column being edited
    item = tree.focus()
    column = tree.identify_column(event.x)
    
    # Get the current value in the cell
    current_value = tree.item(item, "values")[int(column.lstrip("#")) - 1]
    # current_value = tree.item(item, "values")
    print(current_value)
    
    # Create an entry widget to allow editing
    entry = tk.Entry(tree)
    entry.insert(0, current_value)
    
    # Place the entry widget in the cell for editing
    entry.place(relx=0, rely=0, relwidth=0.5, relheight=0.5)
    
    # Function to update the value when editing is done
    def update_value(event):
        new_value = entry.get()
        tree.set(item, column, new_value)
        entry.destroy()
        
    # Bind the update_value function to <Return> and <FocusOut> events
    entry.bind("<Return>", update_value)
    entry.bind("<FocusOut>", update_value)
    entry.focus()

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