from tkinter import *
from tkinter import ttk

class Vehicule:
    def __init__(self, root):
        self.client_frame = Frame(root, width=900, height=600)
        self.client_frame.pack(fill=BOTH, expand=1)

        self.window = Frame(self.client_frame, width=900, height=600)
        self.window.add(self.client_frame, text="Gestionare firme")
        self.window.pack(fill=BOTH, expand=1)
