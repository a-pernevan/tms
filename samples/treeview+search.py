import tkinter as tk
from tkinter import ttk

def search_for_value():
    search_value = search_entry.get()
    found = False
    for item in tree.get_children():
        values = tree.item(item, "values")
        if search_value in values:
            found = True
            search_result.set("Found at row with values: {}".format(values))
            break
    if not found:
        search_result.set("Value not found in any row")

root = tk.Tk()

tree = ttk.Treeview(root)
tree["columns"] = ("Name", "Age", "Location")

# Add some sample data
tree.insert("", tk.END, values=("Alice", 25, "New York"))
tree.insert("", tk.END, values=("Bob", 30, "San Francisco"))
tree.insert("", tk.END, values=("Charlie", 35, "London"))

# Create a search entry and button
search_label = tk.Label(root, text="Enter value to search:")
search_label.pack()
search_entry = tk.Entry(root)
search_entry.pack()

search_button = tk.Button(root, text="Search", command=search_for_value)
search_button.pack()

# Display search result
search_result = tk.StringVar()
search_label = tk.Label(root, textvariable=search_result)
search_label.pack()

root.mainloop()