import tkinter as tk
from tkinter import ttk

def search():
    query = search_entry.get()
    tree.delete(*tree.get_children())
    for data in data_list:
        if query.lower() in str(data).lower():
            tree.insert('', 'end', values=data)

root = tk.Tk()
root.title("Treeview Search Example")

# Create Treeview
tree = ttk.Treeview(root, columns=('Name', 'Age', 'City'))
tree.heading('#0', text='ID')
tree.heading('Name', text='Name')
tree.heading('Age', text='Age')
tree.heading('City', text='City')

# Dummy data
data_list = [
    ('John Doe', 30, 'New York'),
    ('Jane Smith', 25, 'Los Angeles'),
    ('Mike Johnson', 40, 'Chicago'),
    ('Emily Davis', 35, 'San Francisco'),
    ('David Brown', 28, 'Houston')
]

# Insert dummy data
for data in data_list:
    tree.insert('', 'end', values=data)

# Create Search Entry
search_entry = tk.Entry(root)
search_entry.pack()
search_entry.bind('<KeyRelease>', lambda event: search())

tree.pack()
root.mainloop()