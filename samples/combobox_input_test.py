from tkinter import *
from tkinter import ttk


root = Tk()

def print_text():
    print(combo.get())

combo = ttk.Combobox(root)

combo.pack()

but = Button(root, text="test", command=print_text)
but.pack()

root.mainloop()