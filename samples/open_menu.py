from tkinter import *

root = Tk()
root.title("Menu Shortcut Example")
root.geometry("400x300")

def open_menu(event=None):
    menubar = Menu(root)
    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label="New")
    file_menu.add_command(label="Open")
    file_menu.add_command(label="Save")
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menubar)

root.bind('<Control-m>', open_menu)

root.mainloop()
