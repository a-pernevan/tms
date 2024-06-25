from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import os
from dotenv import load_dotenv
from liste import Functii, Filiala

load_dotenv()

class Angajati_firma:
    def __init__(self, master):
        super().__init__()
        # self.master = Toplevel(master)
        # self.master.title("Gestionare angajati")
        self.master = master
        self.master.title("Gestionare angajati")
        self.get_functii = Functii(self.master)
        self.lista_functii = self.get_functii.afisare_functii()
        self.get_filiale = Filiala(self.master)
        self.lista_filiale = self.get_filiale.afisare_filiale()
        if self.lista_functii and self.lista_filiale:
            self.interfata()
        elif not self.lista_functii:
            messagebox.showerror(title="Error", message="No data found")
            self.get_functii.adauga_functie(self.master)

        elif not self.lista_filiale:
            messagebox.showerror(title="Error", message="No data found")
            self.get_filiale.adauga_filiala(self.master)
            self.interfata()

    # Pentur a introduce o noua functie si a actualiza lista
    def refresh_angajati(self):
        self.window = Toplevel(self.master)
        self.window.transient(self.master)
        self.window.grab_set()
        self.get_functii.adauga_functie(self.window)
        self.window.wait_window()
        self.lista_functii = self.get_functii.afisare_functii()
        self.angajat_functie_entry.configure(values=self.lista_functii)
        
        
        
    # Interfata de adaugare angajat nou. 
    def interfata(self):
        self.main_window = LabelFrame(self.master, text="Angajati")
        # self.main_window.grid(row=0, column=0, padx=10, pady=10)
        self.main_window.pack(padx=10, pady=10)
        self.detalii_angajat = LabelFrame(self.main_window, text="Detalii Angajat")
        self.detalii_angajat.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.angajat_nume_label = Label(self.detalii_angajat, text="Nume: ")
        self.angajat_nume_label.grid(row=0, column=0, sticky="nw", pady=10)

        self.angajat_prenume_label = Label(self.detalii_angajat, text="Prenume: ")
        self.angajat_prenume_label.grid(row=1, column=0, sticky="nw", pady=10)

        self.angajat_functie_label = Label(self.detalii_angajat, text="Functie: ")
        self.angajat_functie_label.grid(row=2, column=0, sticky="nw", pady=10)

        self.angajat_filiala_label = Label(self.detalii_angajat, text="Filiala: ")
        self.angajat_filiala_label.grid(row=3, column=0, sticky="nw", pady=10)

        self.angajat_nume_entry = Entry(self.detalii_angajat)
        self.angajat_nume_entry.grid(row=0, column=1, sticky="nw", pady=10, padx=10)

        self.angajat_prenume_entry = Entry(self.detalii_angajat)
        self.angajat_prenume_entry.grid(row=1, column=1, sticky="nw", pady=10, padx=10)

        self.angajat_functie_entry = ttk.Combobox(self.detalii_angajat, values=self.lista_functii)
        # Facem bind la double click pentru a actualiza lista
        self.angajat_functie_entry.bind("<Double-1>", lambda event: self.refresh_angajati())
        self.angajat_functie_entry.grid(row=2, column=1, sticky="nw", pady=10, padx=10)

        self.angajat_filiala = ttk.Combobox(self.detalii_angajat, values=self.lista_filiale)
        self.angajat_filiala.grid(row=3, column=1, sticky="nw", pady=10, padx=10)
        


if __name__ == "__main__":
    root = Tk()
    obj = Angajati_firma(root)
    root.mainloop()

