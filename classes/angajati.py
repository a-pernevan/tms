from optparse import Values
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading
import mysql.connector
import os
from dotenv import load_dotenv
from liste import Functii, Filiala, Lista_orase
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
        self.lista_orase = []
        self.lista_judete = []
        lock = threading.Lock()

        def cauta_oras():
            query = self.oras_entry.get()
            if query:
                filtered_values = [value for value in self.lista_orase if query.lower() in value.lower()]
                # for value, judet in self.lista_orase:
                #     if query.lower() in value.lower():
                #         filtered_orase.append(f"{value}, {judet}")
                #         filtered_judete.append(judet)
                self.oras_entry['values'] = filtered_values
                # # self.judet_entry['values'] = filtered_judete
                # print(filtered_judete)
                # self.judet_entry.set(filtered_orase)

            else:
                self.oras_entry['values'] = self.lista_orase

        def cauta_judet():
            
            query = self.judet_entry.get()
            if query:
                filtered_values = [value for value in self.lista_judete if query.lower() in value.lower()]
                self.judet_entry['values'] = filtered_values
            else:
                self.judet_entry['values'] = self.lista_judete

        def incarca_orase():
            with lock:
                for oras in orase_judete.afisare_orase():
                    # self.lista_orase.append((oras, judet))
                    # self.lista_judete.append(judet)
                    self.lista_orase.append(oras)
                
                for judet in orase_judete.afisare_judete():
                    self.lista_judete.append(judet)


        self.main_window = LabelFrame(self.master, text="Angajati")
        # self.main_window.grid(row=0, column=0, padx=10, pady=10)
        self.main_window.pack(padx=10, pady=10)

        # Frame-ul cu detaliile angajatului.

        self.detalii_angajat = LabelFrame(self.main_window, text="Detalii Angajat")
        self.detalii_angajat.grid(row=0, column=0, padx=5, pady=10, sticky="nw")

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

        self.angajat_id_label = Label(self.detalii_angajat, text="ID: ")
        self.angajat_id_label.grid(row=0, column=4, sticky="nw", pady=10)

        self.angajat_id_entry = Entry(self.detalii_angajat, state="disabled")
        self.angajat_id_entry.grid(row=0, column=5, sticky="nw", pady=10, padx=10)

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

        # Frame date buletin + cnp

        self.buletin_frame = LabelFrame(self.main_window, text="Date C.I. / B.I.")
        self.buletin_frame.grid(row=0, column=1, padx=5, pady=10, sticky="nw")

        self.buletin_no_label = Label(self.buletin_frame, text="Serie / Numar:")
        self.buletin_no_label.grid(row=0, column=0, sticky="nw", pady=10)

        self.buletin_no_entry = Entry(self.buletin_frame)
        self.buletin_no_entry.grid(row=0, column=1, sticky="nw", pady=10, padx=10)

        self.emitent_buletin_label = Label(self.buletin_frame, text="Emitent:")
        self.emitent_buletin_label.grid(row=1, column=0, sticky="nw", pady=10)

        self.emitent_buletin_entry = Entry(self.buletin_frame)
        self.emitent_buletin_entry.grid(row=1, column=1, sticky="nw", pady=10, padx=10)

        self.data_eliberare_buletin_label = Label(self.buletin_frame, text="Data eliberarii:")
        self.data_eliberare_buletin_label.grid(row=2, column=0, sticky="nw", pady=10)

        self.data_eliberare_buletin_entry = DateEntry(self.buletin_frame, locale="RO_ro", date_pattern="yyyy-MM-dd")
        self.data_eliberare_buletin_entry.grid(row=2, column=1, sticky="nw", pady=10, padx=10)

        self.cnp_label = Label(self.buletin_frame, text="CNP:")
        self.cnp_label.grid(row=3, column=0, sticky="nw", pady=10)

        self.cnp_entry = Entry(self.buletin_frame)
        self.cnp_entry.grid(row=3, column=1, sticky="nw", pady=10, padx=10)

        self.cetatenie_label = Label(self.buletin_frame, text="Cetatenie:")
        self.cetatenie_label.grid(row=4, column=0, sticky="nw", pady=10)

        self.cetatenie_entry = Entry(self.buletin_frame)
        self.cetatenie_entry.grid(row=4, column=1, sticky="nw", pady=10, padx=10)

        # Frame cu adresa 

        self.adresa_frame = LabelFrame(self.main_window, text="Date contact")
        self.adresa_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.strada_label = Label(self.adresa_frame, text="Strada:")
        self.strada_label.grid(row=0, column=0, sticky="nw", pady=10)

        self.strada_entry = Entry(self.adresa_frame, width=40)
        self.strada_entry.grid(row=0, column=1, columnspan=7, sticky="nw", pady=10)

        self.nr_strada_label = Label(self.adresa_frame, text="Nr.")
        self.nr_strada_label.grid(row=0, column=8, sticky="nw", pady=10)

        self.nr_strada_entry = Entry(self.adresa_frame, width=5)
        self.nr_strada_entry.grid(row=0, column=9, sticky="nw", pady=10, padx=5)

        self.bloc_label = Label(self.adresa_frame, text="Bloc:")
        self.bloc_label.grid(row=1, column=0, sticky="nw", pady=10)

        self.bloc_entry = Entry(self.adresa_frame, width=5)
        self.bloc_entry.grid(row=1, column=1, sticky="nw", pady=10)

        self.scara_label = Label(self.adresa_frame, text="Sc.")
        self.scara_label.grid(row=1, column=2, sticky="nw", pady=10)

        self.scara_entry = Entry(self.adresa_frame, width=5)
        self.scara_entry.grid(row=1, column=3, sticky="nw", pady=10)

        self.etaj_label = Label(self.adresa_frame, text="Et.")
        self.etaj_label.grid(row=1, column=4, sticky="nw", pady=10)

        self.etaj_entry = Entry(self.adresa_frame, width=5)
        self.etaj_entry.grid(row=1, column=5, sticky="nw", pady=10)

        self.ap_label = Label(self.adresa_frame, text="Ap.")
        self.ap_label.grid(row=1, column=6, sticky="nw", pady=10)

        self.ap_entry = Entry(self.adresa_frame, width=5)
        self.ap_entry.grid(row=1, column=7, sticky="nw", pady=10)

        self.sector_label = Label(self.adresa_frame, text="Sector:")
        self.sector_label.grid(row=2, column=0, sticky="nw", pady=10)

        self.sector_entry = Entry(self.adresa_frame)
        self.sector_entry.grid(row=2, column=1, columnspan=3, sticky="nw", pady=10)

        self.oras_label = Label(self.adresa_frame, text="Oras:")
        self.oras_label.grid(row=3, column=0, sticky="nw", pady=10)

        orase_judete = Lista_orase(self.master)
        thread_orase = threading.Thread(target=incarca_orase)
        thread_orase.start()
        thread_orase.join()

        self.oras_entry = ttk.Combobox(self.adresa_frame, postcommand=cauta_oras)
        self.oras_entry.grid(row=3, column=1, columnspan=3, sticky="nw", pady=10)

        self.judet_label = Label(self.adresa_frame, text="Judet:")
        self.judet_label.grid(row=4, column=0, sticky="nw", pady=10)

        self.judet_entry = ttk.Combobox(self.adresa_frame, postcommand=cauta_judet)
        self.judet_entry.grid(row=4, column=1, columnspan=3, sticky="nw", pady=10)


        self.telefon_personal_label = Label(self.adresa_frame, text="Telefon personal:")
        self.telefon_personal_label.grid(row=0, column=10, sticky="nw", pady=10)

        self.telefon_personal_entry = Entry(self.adresa_frame)
        self.telefon_personal_entry.grid(row=0, column=11, sticky="nw", pady=10, padx=5)

        self.telefon_firma_label = Label(self.adresa_frame, text="Telefon firma:")
        self.telefon_firma_label.grid(row=1, column=10, sticky="nw", pady=10)

        self.telefon_firma_entry = Entry(self.adresa_frame)
        self.telefon_firma_entry.grid(row=1, column=11, sticky="nw", pady=10, padx=5)

        self.email_label = Label(self.adresa_frame, text="Email personal:")
        self.email_label.grid(row=2, column=10, sticky="nw", pady=10)

        self.email_entry = Entry(self.adresa_frame)
        self.email_entry.grid(row=2, column=11, sticky="nw", pady=10, padx=5)

        self.firma_firma_label = Label(self.adresa_frame, text="Email firma:")
        self.firma_firma_label.grid(row=3, column=10, sticky="nw", pady=10)

        self.mail_firma_entry = Entry(self.adresa_frame)
        self.mail_firma_entry.grid(row=3, column=11, sticky="nw", pady=10, padx=5)

        # Frame date permis de conducere

        self.frame_permis = LabelFrame(self.main_window, text="Permis de conducere")
        self.frame_permis.grid(row=1, column=1, sticky="nw", pady=10)

        self.numar_serie_permis_label = Label(self.frame_permis, text="Serie / numar permis:")
        self.numar_serie_permis_label.grid(row=0, column=0, sticky="nw", pady=10)

    
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

