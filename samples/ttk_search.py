import tkinter as tk
from tkinter import ttk

def search_values():
    query = combobox.get()
    if query:
        # Perform search based on the query and update the combobox options
        filtered_values = [value for value in values if query.lower() in value.lower()]
        combobox['values'] = filtered_values
    else:
        combobox['values'] = values

values = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "Yusen"]

root = tk.Tk()

combobox = ttk.Combobox(root, postcommand=search_values)
combobox.pack()

root.mainloop()