from cProfile import label
from distutils.sysconfig import customize_compiler
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading
from dotenv import load_dotenv
from liste import Functii, Filiala, Lista_orase
from tkcalendar import DateEntry
from datetime import date, timedelta, datetime
from utils.tooltip import ToolTip
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
        self.menu_frame = Frame(self.master)
        self.menu_frame.pack(padx=5, pady=5, fill=X, anchor=NW)
        self.main_menu = Menubutton(self.menu_frame, text="Fisier")

        # Cream un meniu principal pentru aplicatie. 
        self.menu = Menu(self.main_menu, tearoff=0)
        self.menu.add_command(label="Angajat nou", accelerator="Ctrl+N", command=self.clear_angajati)
        self.menu.add_command(label="Salvare angajat", accelerator="Ctrl+S", command=self.salvare_angajat)
        self.menu.add_command(label="Editare angajat", accelerator="Ctrl+E", command=self.editare_angajat)
        self.menu.add_separator()
        self.menu.add_command(label="Iesire", command=master.destroy)
        self.main_menu['menu'] = self.menu
        self.menu.entryconfig(0, state="normal")
        self.menu.entryconfig(2, state="disabled")
        
        x = 2

        # Bind-urile pentru meniu si alte shortcut-uri
        self.master.bind("<Control-s>", self.salvare_angajat)
        # probleme la bind-ul asta. 
        # self.master.bind("<Control-d>", lambda x:self.incarca_angajat(x))
        self.master.bind("<Control-e>", self.enable_angajati)
        self.master.bind("<Control-n>", self.clear_angajati)

        self.scadente_menu = Menubutton(self.menu_frame, text="Scadente")
        self.scadente_opt = Menu(self.scadente_menu, tearoff=0)
        self.scadente_menu['menu'] = self.scadente_opt
        self.scadente_opt.add_command(label="Adaugare / editare scadente")
        self.scadente_opt.entryconfig(0, state="disabled")

        self.documente_menu = Menubutton(self.menu_frame, text="Documente")
        self.documente_opt = Menu(self.documente_menu, tearoff=0)
        self.documente_menu['menu'] = self.documente_opt
        self.documente_opt.add_command(label="Adaugare / editare documente")
        self.documente_opt.entryconfig(0, state="disabled")
        
        self.main_menu.grid(row=0, column=0)
        
        self.scadente_menu.grid(row=0, column=1, padx=5)
        self.documente_menu.grid(row=0, column=2, padx=5)
        
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

        self.angajat_status_label = Label(self.detalii_angajat, text="Status: ")
        self.angajat_status_label.grid(row=2, column=4, sticky="nw", pady=10)

        self.angajat_status_check = ttk.Combobox(self.detalii_angajat, values=["Activ", "Inactiv"], width=17)
        self.angajat_status_check.grid(row=2, column=5, sticky="nw", pady=10, padx=10)

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
        self.buletin_frame.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

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

        self.telefon_personal_entry = Entry(self.adresa_frame, width=30)
        self.telefon_personal_entry.grid(row=0, column=11, sticky="nw", pady=10, padx=5)

        self.telefon_firma_label = Label(self.adresa_frame, text="Telefon firma:")
        self.telefon_firma_label.grid(row=1, column=10, sticky="nw", pady=10)

        self.telefon_firma_entry = Entry(self.adresa_frame, width=30)
        self.telefon_firma_entry.grid(row=1, column=11, sticky="nw", pady=10, padx=5)

        self.email_label = Label(self.adresa_frame, text="Email personal:")
        self.email_label.grid(row=2, column=10, sticky="nw", pady=10)

        self.email_entry = Entry(self.adresa_frame, width=30)
        self.email_entry.grid(row=2, column=11, sticky="nw", pady=10, padx=5)

        self.firma_firma_label = Label(self.adresa_frame, text="Email firma:")
        self.firma_firma_label.grid(row=3, column=10, sticky="nw", pady=10)

        self.mail_firma_entry = Entry(self.adresa_frame, width=30)
        self.mail_firma_entry.grid(row=3, column=11, sticky="nw", pady=10, padx=5)

        # Frame date permis de conducere

        self.frame_permis = LabelFrame(self.main_window, text="Permis de conducere")
        self.frame_permis.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.numar_serie_permis_label = Label(self.frame_permis, text="Serie / numar permis:")
        self.numar_serie_permis_label.grid(row=0, column=0, sticky="nw", pady=10)

        self.numar_serie_permis_entry = Entry(self.frame_permis)
        self.numar_serie_permis_entry.grid(row=0, column=1, sticky="nw", pady=10, padx=5)

        self.cat_a = IntVar()
        self.cat_b = IntVar()
        self.cat_c = IntVar()
        self.cat_ce = IntVar()
        self.cat_d = IntVar()
        self.cat_de = IntVar()

        self.cat_a_checkbutton = Checkbutton(self.frame_permis, text="Categorie A", variable=self.cat_a)
        self.cat_a_checkbutton.grid(row=1, column=0, sticky="nw")

        self.cat_b_checkbutton = Checkbutton(self.frame_permis, text="Categorie B", variable=self.cat_b)
        self.cat_b_checkbutton.grid(row=2, column=0, sticky="nw")

        self.cat_c_checkbutton = Checkbutton(self.frame_permis, text="Categorie C", variable=self.cat_c)
        self.cat_c_checkbutton.grid(row=3, column=0, sticky="nw")

        self.cat_ce_checkbutton = Checkbutton(self.frame_permis, text="Categorie C+E", variable=self.cat_ce)
        self.cat_ce_checkbutton.grid(row=4, column=0, sticky="nw")

        self.cat_d_checkbutton = Checkbutton(self.frame_permis, text="Categorie D", variable=self.cat_d)
        self.cat_d_checkbutton.grid(row=5, column=0, sticky="nw")

        self.cat_de_checkbutton = Checkbutton(self.frame_permis, text="Categorie D+E", variable=self.cat_de)
        self.cat_de_checkbutton.grid(row=6, column=0, sticky="nw")


        self.incarca_angajat(2)

    
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

    
    def cat_permis(self, event=None):
        print(self.cat_a.get())

    
    def salvare_angajat(self, event=None, id_angajat=None):
        
        connection._open_connection()
        # Debug
        # print(id_angajat)

        if id_angajat == None:

            sql = "SELECT * FROM angajati WHERE cnp = %s"
            values = (self.cnp_entry.get(), )

            cursor.execute(sql, values)
            result = cursor.fetchall()

            print(result)

            if result:
                messagebox.showinfo(title="Eroare", message="Angajatul exista deja!")
                return


            sql = """INSERT INTO angajati (nume, prenume, functie, filiala, status_angajat, 
                        data_angajare, data_nastere, zile_concediu, casatorit, copii, 
                        buletin, emitent_buletin, data_buletin, cnp, cetatenie, strada, 
                        nr_strada, bloc, scara, etaj, apartament, 
                        sector, oras_domiciliu, judet_domiciliu, tel_personal, tel_firma, 
                        email_personal, email_firma, permis_auto, categ_a, 
                        categ_b, categ_c, categ_ce, categ_d, categ_de) VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                
            values = (self.angajat_nume_entry.get(), self.angajat_prenume_entry.get(), self.angajat_functie_entry.get(), \
                        self.angajat_filiala.get(), self.angajat_status_check.get(), self.data_angajare_entry.get_date(), \
                        self.data_nastere_entry.get_date(), self.zile_concediu_entry.get(), self.casatorit.get(), self.copii_entry.get(), \
                            self.buletin_no_entry.get(), self.emitent_buletin_entry.get(), self.data_eliberare_buletin_entry.get_date(), \
                            self.cnp_entry.get(), self.cetatenie_entry.get(), self.strada_entry.get(), self.nr_strada_entry.get(), self.bloc_entry.get(), \
                            self.scara_entry.get(), self.etaj_entry.get(), self.ap_entry.get(), self.sector_entry.get(), self.oras_entry.get(), \
                            self.judet_entry.get(), self.telefon_personal_entry.get(), self.telefon_firma_entry.get(), self.email_entry.get(), self.mail_firma_entry.get(), \
                            self.numar_serie_permis_entry.get(), self.cat_a.get(), self.cat_b.get(), self.cat_c.get(), self.cat_ce.get(), self.cat_d.get(), \
                            self.cat_de.get())
            try:
                
                cursor.execute(sql, values)

                connection.commit()

                messagebox.showinfo("Salvare", "Salvare reusita")
            
            except:
                messagebox.showerror("Eroare", "Eroare la inserare angajat")
            # except:
            #     messagebox.showerror("Eroare", "Eroare la inserare angajat")

            finally:
                connection.close()

            try:
                connection._open_connection()
                sql = "SELECT id from angajati ORDER BY id DESC LIMIT 1"

                cursor.execute(sql)
                self.angajat_id_entry.config(state=NORMAL)
                self.angajat_id_entry.delete(0, END)
                self.angajat_id_entry.insert(0, cursor.fetchone()[0])
                self.angajat_id_entry.config(state=DISABLED)

            except:
                messagebox.showerror("Eroare", "Eroare la generare ID")

        else:
            sql = "DELETE FROM angajati WHERE id = %s"
            values = (id_angajat,)
            cursor.execute(sql, values)
            connection.commit()
            sql = """INSERT INTO angajati (id, nume, prenume, functie, filiala, status_angajat, 
                        data_angajare, data_nastere, zile_concediu, casatorit, copii, 
                        buletin, emitent_buletin, data_buletin, cnp, cetatenie, strada, 
                        nr_strada, bloc, scara, etaj, apartament, 
                        sector, oras_domiciliu, judet_domiciliu, tel_personal, tel_firma, 
                        email_personal, email_firma, permis_auto, categ_a, 
                        categ_b, categ_c, categ_ce, categ_d, categ_de) VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                
            values = (id_angajat, self.angajat_nume_entry.get(), self.angajat_prenume_entry.get(), self.angajat_functie_entry.get(), \
                        self.angajat_filiala.get(), self.angajat_status_check.get(), self.data_angajare_entry.get_date(), \
                        self.data_nastere_entry.get_date(), self.zile_concediu_entry.get(), self.casatorit.get(), self.copii_entry.get(), \
                            self.buletin_no_entry.get(), self.emitent_buletin_entry.get(), self.data_eliberare_buletin_entry.get_date(), \
                            self.cnp_entry.get(), self.cetatenie_entry.get(), self.strada_entry.get(), self.nr_strada_entry.get(), self.bloc_entry.get(), \
                            self.scara_entry.get(), self.etaj_entry.get(), self.ap_entry.get(), self.sector_entry.get(), self.oras_entry.get(), \
                            self.judet_entry.get(), self.telefon_personal_entry.get(), self.telefon_firma_entry.get(), self.email_entry.get(), self.mail_firma_entry.get(), \
                            self.numar_serie_permis_entry.get(), self.cat_a.get(), self.cat_b.get(), self.cat_c.get(), self.cat_ce.get(), self.cat_d.get(), \
                            self.cat_de.get())
            print(sql)
            print(values)
            try:
                
                cursor.execute(sql, values)

                connection.commit()

                messagebox.showinfo("Modificare", "Angajatul a fost modificat")
            
            except:
                messagebox.showerror("Eroare", "Eroare la modificare angajat")
            # except:
            #     messagebox.showerror("Eroare", "Eroare la inserare angajat")

            finally:
                connection.close()

            try:
                self.incarca_angajat(id_angajat)

            except:
                messagebox.showerror("Eroare", "eroare la incarcare.")


    def disable_angajati(self, event=None):
        self.angajat_nume_entry.config(state=DISABLED)
        self.angajat_prenume_entry.config(state=DISABLED)
        self.angajat_functie_entry.config(state=DISABLED)
        self.angajat_filiala.config(state=DISABLED)
        self.angajat_status_check.config(state=DISABLED)
        self.data_angajare_entry.config(state=DISABLED)
        self.data_nastere_entry.config(state=DISABLED)
        self.zile_concediu_entry.config(state=DISABLED)
        self.casatorit_check.config(state=DISABLED)
        self.copii_entry.config(state=DISABLED)
        self.buletin_no_entry.config(state=DISABLED)
        self.emitent_buletin_entry.config(state=DISABLED)
        self.data_eliberare_buletin_entry.config(state=DISABLED)
        self.cnp_entry.config(state=DISABLED)
        self.cetatenie_entry.config(state=DISABLED)
        self.strada_entry.config(state=DISABLED)
        self.nr_strada_entry.config(state=DISABLED)
        self.bloc_entry.config(state=DISABLED)
        self.scara_entry.config(state=DISABLED)
        self.etaj_entry.config(state=DISABLED)
        self.ap_entry.config(state=DISABLED)
        self.sector_entry.config(state=DISABLED)
        self.oras_entry.config(state=DISABLED)
        self.judet_entry.config(state=DISABLED)
        self.telefon_personal_entry.config(state=DISABLED)
        self.telefon_firma_entry.config(state=DISABLED)
        self.email_entry.config(state=DISABLED)
        self.mail_firma_entry.config(state=DISABLED)
        self.numar_serie_permis_entry.config(state=DISABLED)
        self.cat_a_checkbutton.config(state=DISABLED)
        self.cat_b_checkbutton.config(state=DISABLED)
        self.cat_c_checkbutton.config(state=DISABLED)
        self.cat_ce_checkbutton.config(state=DISABLED)
        self.cat_d_checkbutton.config(state=DISABLED)
        self.cat_de_checkbutton.config(state=DISABLED)

    
    # Activam toate entry-urile
    def enable_angajati(self, event=None):
        self.angajat_nume_entry.config(state=NORMAL)
        self.angajat_prenume_entry.config(state=NORMAL)
        self.angajat_functie_entry.config(state=NORMAL)
        self.angajat_filiala.config(state=NORMAL)
        self.angajat_status_check.config(state=NORMAL)
        self.data_angajare_entry.config(state=NORMAL)
        self.data_nastere_entry.config(state=NORMAL)
        self.zile_concediu_entry.config(state=NORMAL)
        self.casatorit_check.config(state=NORMAL)
        self.copii_entry.config(state=NORMAL)
        self.buletin_no_entry.config(state=NORMAL)
        self.emitent_buletin_entry.config(state=NORMAL)
        self.data_eliberare_buletin_entry.config(state=NORMAL)
        self.cnp_entry.config(state=NORMAL)
        self.cetatenie_entry.config(state=NORMAL)
        self.strada_entry.config(state=NORMAL)
        self.nr_strada_entry.config(state=NORMAL)
        self.bloc_entry.config(state=NORMAL)
        self.scara_entry.config(state=NORMAL)
        self.etaj_entry.config(state=NORMAL)
        self.ap_entry.config(state=NORMAL)
        self.sector_entry.config(state=NORMAL)
        self.oras_entry.config(state=NORMAL)
        self.judet_entry.config(state=NORMAL)
        self.telefon_personal_entry.config(state=NORMAL)
        self.telefon_firma_entry.config(state=NORMAL)
        self.email_entry.config(state=NORMAL)
        self.mail_firma_entry.config(state=NORMAL)
        self.numar_serie_permis_entry.config(state=NORMAL)
        self.cat_a_checkbutton.config(state=NORMAL)
        self.cat_b_checkbutton.config(state=NORMAL)
        self.cat_c_checkbutton.config(state=NORMAL)
        self.cat_ce_checkbutton.config(state=NORMAL)
        self.cat_d_checkbutton.config(state=NORMAL)
        self.cat_de_checkbutton.config(state=NORMAL)
        self.menu.entryconfig(1, state="normal")
        self.menu.entryconfig(0, state="normal")
        self.menu.entryconfig(2, state="disabled")


    
    # Golim toate entry-urile
    def clear_angajati(self, event=None):
        self.enable_angajati()
        self.angajat_nume_entry.delete(0, END)
        self.angajat_prenume_entry.delete(0, END)
        self.angajat_id_entry.config(state=NORMAL)
        self.angajat_id_entry.delete(0, END)
        self.angajat_id_entry.config(state=DISABLED)
        self.angajat_functie_entry.delete(0, END)
        self.angajat_filiala.set('')
        self.angajat_status_check.set('')
        self.data_angajare_entry.delete(0, END)
        self.data_nastere_entry.delete(0, END)
        self.zile_concediu_entry.delete(0, END)
        self.casatorit_check.deselect()
        self.copii_entry.delete(0, END)
        self.buletin_no_entry.delete(0, END)
        self.emitent_buletin_entry.delete(0, END)
        self.data_eliberare_buletin_entry.delete(0, END)
        self.cnp_entry.delete(0, END)
        self.cetatenie_entry.delete(0, END)
        self.strada_entry.delete(0, END)
        self.nr_strada_entry.delete(0, END)
        self.bloc_entry.delete(0, END)
        self.scara_entry.delete(0, END)
        self.etaj_entry.delete(0, END)
        self.ap_entry.delete(0, END)
        self.sector_entry.delete(0, END)
        self.oras_entry.delete(0, END)
        self.judet_entry.delete(0, END)
        self.telefon_personal_entry.delete(0, END)
        self.telefon_firma_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.mail_firma_entry.delete(0, END)
        self.numar_serie_permis_entry.delete(0, END)
        self.cat_a_checkbutton.deselect()
        self.cat_b_checkbutton.deselect()
        self.cat_c_checkbutton.deselect()
        self.cat_ce_checkbutton.deselect()
        self.cat_d_checkbutton.deselect()
        self.cat_de_checkbutton.deselect()    


    
    # Incarcam datele angajatului din baza de date
    def incarca_angajat(self, id_angajat, event=None):
        print(id_angajat)
        self.clear_angajati()
        try:
            connection._open_connection()
            sql = "SELECT * FROM angajati WHERE id = %s"
            values = (id_angajat,)
            cursor.execute(sql, values)
            result = cursor.fetchone()

        except:
            messagebox.showerror("Eroare", "Ceva nu a functionat!", parent=self.master)

        finally:
            connection.close()

        self.enable_angajati()

        self.angajat_nume_entry.insert(0, result[1])
        self.angajat_prenume_entry.insert(0, result[2])
        self.angajat_id_entry.config(state=NORMAL)
        self.angajat_id_entry.delete(0, END)
        self.angajat_id_entry.insert(0, result[0])
        self.angajat_id_entry.config(state=DISABLED)
        self.angajat_functie_entry.set(result[3])
        self.angajat_filiala.set(result[4])
        self.angajat_status_check.set(result[5])
        self.data_angajare_entry.set_date(result[6])
        self.vechime_angajat()
        self.data_nastere_entry.set_date(result[7])
        self.varsta_angajat()
        self.zile_concediu_entry.insert(0, result[8])
        self.casatorit.set(result[9])
        self.copii_entry.insert(0, result[10])
        self.buletin_no_entry.insert(0, result[11])
        self.emitent_buletin_entry.insert(0, result[12])
        self.data_eliberare_buletin_entry.set_date(result[13])
        self.cnp_entry.insert(0, result[14])
        self.cetatenie_entry.insert(0, result[15])
        self.strada_entry.insert(0, result[16])
        self.nr_strada_entry.insert(0, result[17])
        self.bloc_entry.insert(0, result[18])
        self.scara_entry.insert(0, result[19])
        self.etaj_entry.insert(0, result[20])
        self.ap_entry.insert(0, result[21])
        self.sector_entry.insert(0, result[22])
        self.oras_entry.insert(0, result[23])
        self.judet_entry.insert(0, result[24])
        self.telefon_personal_entry.insert(0, result[25])
        self.telefon_firma_entry.insert(0, result[26])
        self.email_entry.insert(0, result[27])
        self.mail_firma_entry.insert(0, result[28])
        self.numar_serie_permis_entry.insert(0, result[29])
        self.cat_a.set(result[30])
        self.cat_b.set(result[31])
        self.cat_c.set(result[32])
        self.cat_ce.set(result[33])
        self.cat_d.set(result[34])
        self.cat_de.set(result[35])

        self.disable_angajati()
        self.menu.entryconfig(1, state="disabled")
        self.menu.entryconfig(2, state="normal")

    def editare_angajat(self, event=None):
        self.enable_angajati()
        self.menu.entryconfig(1, state="normal", label="Actualizare angajat", accelerator="Ctrl+D", command=lambda: self.salvare_angajat(id_angajat=self.angajat_id_entry.get()))
        self.menu.entryconfig(2, state="disabled")

if __name__ == "__main__":
    root = Tk()
    obj = Angajati_firma(root)
    root.mainloop()

