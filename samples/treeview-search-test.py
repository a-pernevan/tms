import tkinter as tk
from tkinter import ttk

def search():
    query = search_entry.get()
    for child in tree.get_children():
        if query.lower() in str(tree.item(child)['values']).lower():
            tree.selection_set(child)
        else:
            tree.selection_remove(child)

root = tk.Tk()
root.title("Treeview Search Example")

# Create Treeview
tree = ttk.Treeview(root, columns=('Name', 'Age', 'City'))
tree.heading('#0', text='ID')
tree.heading('Name', text='Name')
tree.heading('Age', text='Age')
tree.heading('City', text='City')

# Insert some dummy data
for i in range(10):
    tree.insert('', 'end', text=str(i), values=('John Doe', 30, 'New York'))

# Create Search Entry
search_entry = tk.Entry(root)
search_entry.pack()
search_entry.bind('<KeyRelease>', lambda event: search())

tree.pack()
root.mainloop()