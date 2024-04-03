from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class Clients:
    def __init__(self, root):
        main_window = ttk.Notebook(root)
        main_window.pack(pady=0)

        main_frame = Frame(main_window, width=900, height=600)
        client_frame = Frame(main_window, width=900, height=600)

        main_frame.pack(fill=BOTH, expand=1)
        client_frame.pack(fill=BOTH, expand=1)

        main_window.add(main_frame, text="Principal")
        main_window.add(client_frame, text="Gestionare clienti")
        