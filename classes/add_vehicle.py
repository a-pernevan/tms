from tkinter import *
from tkinter import ttk

class Vehicule:
    def __init__(self, root):
        self.client_frame = Frame(root, width=900, height=600)
        self.client_frame.pack(fill=BOTH, expand=1)

        self.vehicule_frame = LabelFrame(self.client_frame, text="Vehicule")
        self.vehicule_frame.grid(row=0, column=0, sticky="nw")


if __name__ == "__main__":
    root = Tk()
    root.title("Adaugare Vehicul")
    root.geometry("900x600")

    hello = Vehicule(root)

    root.mainloop()
