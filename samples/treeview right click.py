import tkinter as tk
from tkinter import ttk
from tkinter import Menu

root = tk.Tk()
root.geometry("400x400")

tree = ttk.Treeview(root)
tree.pack()

def show_menu(event):
    menu = Menu(root, tearoff=0)
    menu.add_command(label="Edit", command=edit_item)
    menu.add_command(label="Delete", command=delete_item)
    menu.post(event.x_root, event.y_root)

def edit_item():
    # Code to edit the selected item
    pass

def delete_item():
    # Code to delete the selected item
    pass

tree.bind("<Button-3>", show_menu)

root.mainloop()
