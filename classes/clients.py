from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from classes.add_vehicle import Vehicule

class Clients:
    def __init__(self, root):
        self.main_window = ttk.Notebook(root)
        self.main_window.pack(pady=0)

        self.main_frame = Frame(self.main_window, width=900, height=600)
        self.client_frame = Frame(self.main_window, width=900, height=600)

        self.main_frame.pack(fill=BOTH, expand=1)
        self.client_frame.pack(fill=BOTH, expand=1)

        self.main_window.add(self.main_frame, text="Principal")
        self.main_window.add(self.client_frame, text="Gestionare firme")
        self.adaugare_cam = Button(self.main_frame, text="Adaugare", command=self.adaugare)
        self.adaugare_cam.pack()

    def adaugare(self):
        Vehicule(self.main_window)