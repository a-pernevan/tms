from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import os
from dotenv import load_dotenv
from liste import Functii

load_dotenv()

class Angajati_firma:
    def __init__(self, master):
        super().__init__()
        self.master = Toplevel(master)
        self.master.title("Gestionare angajati")
        self.get_functii = Functii(self.master)
        self.lista_functii = self.get_functii.afisare_functii()
        if self.lista_functii:
            self.interfata()
        else:
            messagebox.showerror(title="Error", message="No data found")
            self.get_functii.adauga_functie(self.master)

    def interfata(self):
        self.main_window = LabelFrame(self.master, text="Angajati")
        self.main_window.pack(padx=10, pady=10)
        self.detalii_angajat = LabelFrame(self.main_window, text="Detalii Angajat")
        self.detalii_angajat.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.angajat_nume_label = Label(self.detalii_angajat, text="Nume: ")
        self.angajat_nume_label.grid(row=0, column=0, sticky="nw", pady=10)

        self.angajat_prenume_label = Label(self.detalii_angajat, text="Prenume: ")
        self.angajat_prenume_label.grid(row=1, column=0, sticky="nw", pady=10)

        self.angajat_functie_label = Label(self.detalii_angajat, text="Functie: ")
        self.angajat_functie_label.grid(row=2, column=0, sticky="nw")

        self.angajat_nume_entry = Entry(self.detalii_angajat)
        self.angajat_nume_entry.grid(row=0, column=1, sticky="nw", pady=10, padx=10)

        self.angajat_prenume_entry = Entry(self.detalii_angajat)
        self.angajat_prenume_entry.grid(row=1, column=1, sticky="nw", pady=10, padx=10)

        self.angajat_functie_entry = ttk.Combobox(self.detalii_angajat, values=self.lista_functii)
        self.angajat_functie_entry.grid(row=2, column=1, sticky="nw", pady=10, padx=10)


if __name__ == "__main__":
    root = Tk()
    obj = Angajati_firma(root)
    root.mainloop()

