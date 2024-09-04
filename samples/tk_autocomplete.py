import tkinter as tk
from tkinter import ttk

# Sample database (replace with your actual database query)
database = ["apple", "banana", "cherry", "date", "elderberry"]

class AutocompleteEntry(ttk.Combobox):
    def __init__(self, master, database):
        super().__init__(master)
        self.database = database
        self['values'] = database

    def autocomplete(self, input_str):
        if input_str:
            self['values'] = [item for item in self.database if item.startswith(input_str)]
        else:
            self['values'] = self.database

root = tk.Tk()
entry = AutocompleteEntry(root, database)

def check_input():
    input_str = entry.get()
    entry.autocomplete(input_str)
    root.after(100, check_input)  # Repeat every 100ms

check_input()
entry.pack()
root.mainloop()