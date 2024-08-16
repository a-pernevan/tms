import tkinter as tk
from tkinter import ttk

def show_treeview(selected_value):
    # Create a new toplevel window
    popup = tk.Toplevel(root)
    popup.title("Treeview")

    # Create a treeview
    tree = ttk.Treeview(popup)
    tree["columns"] = ("Column 1", "Column 2")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Column 1", anchor=tk.W, width=100)
    tree.column("Column 2", anchor=tk.W, width=100)
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("Column 1", text="Column 1", anchor=tk.W)
    tree.heading("Column 2", text="Column 2", anchor=tk.W)
    tree.insert("", "end", values=("Value 1", "Value 2"))
    tree.pack()

    def on_tree_select(event):
        # Get the selected item from the treeview
        selected_item = tree.selection()[0]
        selected_value = tree.item(selected_item, "values")[0]

        # Update the dropdown value
        variable.set(selected_value)

        # Close the treeview window
        popup.destroy()

    tree.bind("<ButtonRelease-1>", on_tree_select)

    # Create the main window
root = tk.Tk()
root.title("Dropdown")

# Create a dropdown
variable = tk.StringVar(root)
variable.set(" ")  # default value
# options = ["Option 1", "Option 2", "Option 3"]
options = [" ", "Please select"]
dropdown = ttk.OptionMenu(root, variable, *options, command=show_treeview)
dropdown.pack()

root.mainloop()