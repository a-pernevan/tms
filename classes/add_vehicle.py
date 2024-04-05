from tkinter import *
from tkinter import ttk

class Vehicule:
    def __init__(self, root):
        self.main_window = Frame(root)
        # self.main_window.title("Adaugare mijloc transport")
        # self.main_window.geometry("900x600")
        self.test = Button(root, text="test")
        self.test.pack()