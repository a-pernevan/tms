from ttkwidgets.autocomplete import AutocompleteEntry
import tkinter as tk

window = tk.Tk()
tk.Label(window, text="Entry with autocompletion for the Tk instance's methods:").pack(side='left')
entry = AutocompleteEntry(window, width=20, completevalues=dir(window))
entry.pack(side='right')
window.mainloop()

