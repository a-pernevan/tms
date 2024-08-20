from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import os
from dotenv import load_dotenv
from liste import Functii, Filiala
from tkcalendar import DateEntry
from datetime import date, timedelta, datetime
try:
    from database.datab import connection, cursor
except:
    mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server, program will exit")
    quit()

load_dotenv()

class Angajati_firma:
    def __init__(self, master):
        super().__init__()
        # self.master = Toplevel(master)
        # self.master.title("Gestionare angajati")
        self.master = master
        # self.master.title("Gestionare angajati")
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

    # Pentur a introduce o noua functie si a actualiza lista
    def refresh_angajati(self):
        self.window = Toplevel(self.master)
        self.window.transient(self.master)
        self.window.grab_set()
        self.get_functii.adauga_functie(self.window)
        self.window.wait_window()
        self.lista_functii = self.get_functii.afisare_functii()
        self.angajat_functie_entry.configure(values=self.lista_functii)
        
    def refresh_filiale(self):
        window = Toplevel(self.master)
        window.transient(self.master)
        window.grab_set()
        self.get_filiale.adauga_filiala(window)
        window.wait_window()
        lista_filiale = self.get_filiale.afisare_filiale()
        self.angajat_filiala.configure(values=lista_filiale)    
        
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
        self.angajat_prenume_label.grid(row=0, column=2, sticky="nw", pady=10)

        self.angajat_functie_label = Label(self.detalii_angajat, text="Functie: ")
        self.angajat_functie_label.grid(row=2, column=0, sticky="nw", pady=10)

        self.angajat_filiala_label = Label(self.detalii_angajat, text="Filiala: ")
        self.angajat_filiala_label.grid(row=2, column=2, sticky="nw", pady=10)

        self.angajat_nume_entry = Entry(self.detalii_angajat)
        self.angajat_nume_entry.grid(row=0, column=1, sticky="nw", pady=10, padx=10)

        self.angajat_prenume_entry = Entry(self.detalii_angajat)
        self.angajat_prenume_entry.grid(row=0, column=3, sticky="nw", pady=10, padx=10)

        self.angajat_functie_entry = ttk.Combobox(self.detalii_angajat, values=self.lista_functii, width=17)
        # Facem bind la double click pentru a actualiza lista
        self.angajat_functie_entry.bind("<Double-1>", lambda event: self.refresh_angajati())
        self.angajat_functie_entry.grid(row=2, column=1, sticky="nw", pady=10, padx=10)

        self.angajat_filiala = ttk.Combobox(self.detalii_angajat, values=self.lista_filiale, width=17)
        self.angajat_filiala.bind("<Double-1>", lambda event: self.refresh_filiale())
        self.angajat_filiala.grid(row=2, column=3, sticky="nw", pady=10, padx=10)

        self.data_angajare_label = Label(self.detalii_angajat, text="Data angajare: ")
        self.data_angajare_label.grid(row=4, column=0, sticky="nw", pady=10)

        self.data_angajare_entry = DateEntry(self.detalii_angajat, locale="RO_ro", date_pattern="yyyy-MM-dd")
        self.data_angajare_entry.grid(row=4, column=1, sticky="nw", pady=10, padx=10)

        self.data_angajare_entry.bind("<<DateEntrySelected>>", lambda event: self.vechime_angajat())

        self.vechime_angajat_label = Label(self.detalii_angajat, text="Vechime angajat: ")
        self.vechime_angajat_label.grid(row=4, column=2, sticky="w", pady=10)

        self.vechime_angajat_entry = Entry(self.detalii_angajat, state=DISABLED)
        self.vechime_angajat_entry.grid(row=4, column=3, sticky="nw", pady=10, padx=10)

        self.data_nastere_label = Label(self.detalii_angajat, text="Data nastere: ")
        self.data_nastere_label.grid(row=5, column=0, sticky="nw", pady=10)

        self.data_nastere_entry = DateEntry(self.detalii_angajat, locale="RO_ro", date_pattern="yyyy-MM-dd")
        self.data_nastere_entry.grid(row=5, column=1, sticky="nw", pady=10, padx=10)

        self.data_nastere_entry.bind("<<DateEntrySelected>>", lambda event: self.varsta_angajat())

        self.varsta_label = Label(self.detalii_angajat, text="Varsta: ")
        self.varsta_label.grid(row=5, column=2, sticky="w", pady=10)

        self.varsta_entry = Entry(self.detalii_angajat, state=DISABLED)
        self.varsta_entry.grid(row=5, column=3, sticky="nw", pady=10, padx=10)

        self.zile_concediu_label = Label(self.detalii_angajat, text="Zile concediu: ")
        self.zile_concediu_label.grid(row=5, column=4, sticky="nw", pady=10)

        self.zile_concediu_entry = Entry(self.detalii_angajat)
        self.zile_concediu_entry.grid(row=5, column=5, sticky="nw", pady=10, padx=10)

        self.casatorit_label = Label(self.detalii_angajat, text="Casatorit: ")
        self.casatorit_label.grid(row=6, column=0, sticky="nw", pady=10)

        self.casatorit = IntVar()

        self.casatorit_check = Checkbutton(self.detalii_angajat, text="", variable=self.casatorit)
        self.casatorit_check.deselect()
        self.casatorit_check.grid(row=6, column=1, sticky="nw", pady=10, padx=10)

        self.copii_label = Label(self.detalii_angajat, text="Copii: ")
        self.copii_label.grid(row=6, column=2, sticky="w", pady=10)

        self.copii_entry = Entry(self.detalii_angajat)
        self.copii_entry.grid(row=6, column=3, sticky="nw", pady=10, padx=10)


    
    def vechime_angajat(self):

        today_date = datetime.strptime(date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        print(today_date)

        angajare_date = datetime.strptime(str(self.data_angajare_entry.get_date()), "%Y-%m-%d")
        
        vechime = (datetime.now() - angajare_date).days // 365
        
        print(vechime)
        self.vechime_angajat_entry.config(state=NORMAL)
        self.vechime_angajat_entry.delete(0, END)
        self.vechime_angajat_entry.insert(0, vechime)
        self.vechime_angajat_entry.config(state=DISABLED)

    
    def varsta_angajat(self):
        today_date = datetime.strptime(date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")

        nastere_date = datetime.strptime(str(self.data_nastere_entry.get_date()), "%Y-%m-%d")
        varsta = (datetime.now() - nastere_date).days // 365

        self.varsta_entry.config(state=NORMAL)
        self.varsta_entry.delete(0, END)
        self.varsta_entry.insert(0, varsta)
        self.varsta_entry.config(state=DISABLED)

if __name__ == "__main__":
    root = Tk()
    obj = Angajati_firma(root)
    root.mainloop()

