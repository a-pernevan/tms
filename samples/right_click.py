import tkinter as tk
from tkinter import Menu
import tkinter.ttk as ttk

def create_context_menu(entry_widget):
    def copy_text():
        entry_widget.event_generate('<<Copy>>')

    def cut_text():
        entry_widget.event_generate('<<Cut>>')

    def paste_text():
        entry_widget.event_generate('<<Paste>>')

    context_menu = Menu(entry_widget, tearoff=0)
    context_menu.add_command(label="Copy", command=copy_text)
    context_menu.add_command(label="Cut", command=cut_text)
    context_menu.add_command(label="Paste", command=paste_text)

    def show_context_menu(event):
        context_menu.post(event.x_root, event.y_root)

    entry_widget.bind("<Button-3>", show_context_menu)

root = tk.Tk()

entry1 = ttk.Entry(root)
entry1.pack()
create_context_menu(entry1)

entry2 = ttk.Entry(root)
entry2.pack()
create_context_menu(entry2)

root.mainloop()