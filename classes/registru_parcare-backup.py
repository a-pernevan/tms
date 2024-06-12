from calendar import c
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import os
from dotenv import load_dotenv
from tkcalendar import DateEntry
import time
try:
    from database.datab import connection, cursor
except:
    mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server, program will exit")
    quit()
class Registru_parcare:
    def __init__(self, master):
        super().__init__()
        load_dotenv()
        # Variabila pentru adaugare manuala vizitator
        self.visit_manual = False        

        # Valori demo pt nr camion
        self.truck_plate = []
        cursor.execute("SELECT plate_no FROM tauros_truck WHERE categorie='AUTOTRACTOR' OR categorie='AUTOTURISM'")

        self.nr_auto_cap = cursor.fetchall()
        # cursor.close()
        # connection.close()
        # Filtram numerele de cap pentru a le afisa

        for truck in self.nr_auto_cap:
            self.truck_plate.append(truck[0])


        # Cream interfata si notebook-ul
        # self.master = master
        # self.master.title("Registru parcare")
        self.main_window = ttk.Notebook(master, width=1280, height=800)
        self.main_window.pack(pady=0)

        # Cream cele trei frame-uri

        self.tauros_frame = Frame(self.main_window)
        self.tauros_frame.pack(fill=BOTH, expand=1, anchor=W)

        self.samsung_frame = Frame(self.main_window)
        self.samsung_frame.pack(fill=BOTH, expand=1, anchor=W)

        self.vizitatori_frame = Frame(self.main_window)
        self.vizitatori_frame.pack(fill=BOTH, expand=1, anchor=W)

        self.main_window.add(self.tauros_frame, text="Tauros")
        self.main_window.add(self.samsung_frame, text="Samsung")
        self.main_window.add(self.vizitatori_frame, text="Vizitatori")

        # Frame-ul parcare tauros

        self.logo_frame = Frame(self.tauros_frame)
        self.logo_frame.pack()

        self.logo_title = Label(self.logo_frame, text="Intrari / Iesiri Parcare Principala TAUROS", font=("Arial", 20))
        self.logo_title.pack()

        self.truck_frame = Frame(self.tauros_frame)
        self.truck_frame.pack(pady=10)

        self.nr_auto_label = Label(self.truck_frame, text="Nr auto:")
        self.nr_auto_label.grid(row=0, column=0, padx=5)

        self.remorca_label = Label(self.truck_frame, text="Remorca:")
        self.remorca_label.grid(row=0, column=2, padx=5, sticky="w")

        self.n = StringVar()
        self.nr_auto_combo = ttk.Combobox(self.truck_frame, postcommand=self.search_auto, textvariable=self.n)
        self.nr_auto_combo.grid(row=0, column=1)

        # self.nr_auto_entry = Entry(self.truck_frame, width=23)
        # self.nr_auto_entry.grid(row=0, column=1, padx=5, sticky="w")

        self.remorca_combo = ttk.Combobox(self.truck_frame, width=23, postcommand=self.search_remorca)
        self.remorca_combo.grid(row=0, column=3, sticky="w")

        self.lpr_label = Label(self.truck_frame, text="LPR:")
        self.lpr_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.lpr_input = Entry(self.truck_frame, width=23)
        self.lpr_input.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.test_button = Button(self.truck_frame, text="Verifica nr auto", command=self.search_lpr)
        self.test_button.grid(row=1, column=2, padx=5, pady=5, sticky="w", columnspan=2)

        # self.test_button = Button(self.tauros_frame, text="Test")
        # self.test_button.grid(row=0, column=0)

        # Frame samsung - interfata

        self.samsung_logo_frame = Frame(self.samsung_frame)
        self.samsung_logo_frame.pack()

        self.samsung_logo_title = Label(self.samsung_logo_frame, text="Intrari / Iesiri Samsung", font=("Arial", 20))
        self.samsung_logo_title.pack()

        self.samsung_reg_frame = Frame(self.samsung_frame)
        self.samsung_reg_frame.pack(pady=10)

        self.sam_plate_no_label = Label(self.samsung_reg_frame, text="Nr Auto:")
        self.sam_plate_no_label.grid(row=0, column=0, padx=5, sticky="w")

        self.sam_plate_no_entry = Entry(self.samsung_reg_frame, width=23, state="readonly")
        self.sam_plate_no_entry.grid(row=0, column=1, padx=5, sticky="w")

        self.park_place_label = Label(self.samsung_reg_frame, text="Transportator:")
        self.park_place_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.park_place = Entry(self.samsung_reg_frame, width=23, state="readonly")
        self.park_place.grid(row=0, column=3, padx=5, sticky="w")

        self.sam_nume_label = Label(self.samsung_reg_frame, text="Nume sofer:")
        self.sam_nume_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.sam_nume_entry = Entry(self.samsung_reg_frame, width=23, state="readonly")
        self.sam_nume_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.sam_prenume_label = Label(self.samsung_reg_frame, text="Prenume sofer:")
        self.sam_prenume_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.sam_prenume_entry = Entry(self.samsung_reg_frame, width=23, state="readonly")
        self.sam_prenume_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.sam_seal_label = Label(self.samsung_reg_frame, text="Sigiliu:")
        self.sam_seal_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.sam_seal_entry = Entry(self.samsung_reg_frame, width=23, state="readonly")
        self.sam_seal_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.sam_id_label = Label(self.samsung_reg_frame, text="ID:")
        self.sam_id_label.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        self.sam_save_button = Button(self.samsung_reg_frame, text="Salveaza", state="disabled", command=self.samsung_save)
        self.sam_save_button.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        # Frame samsung - tabelul treeview

        self.sam_table_frame = Frame(self.samsung_frame)
        self.sam_table_frame.pack(pady=10)

        self.sam_table = ttk.Treeview(self.sam_table_frame)
        self.sam_table["columns"] = ("Nr Auto", "Transportator", "Nume sofer", "Prenume sofer", "Sigiliu", "Data intrare", "Data iesire", "Durata parcare", "Status")
        self.sam_table.column("#0", width=50, stretch=NO)
        self.sam_table.column("Nr Auto", anchor=CENTER, width=100)
        self.sam_table.column("Transportator", anchor=CENTER, width=100)
        self.sam_table.column("Nume sofer", anchor=CENTER, width=100)
        self.sam_table.column("Prenume sofer", anchor=CENTER, width=100)
        self.sam_table.column("Sigiliu", anchor=CENTER, width=100)
        self.sam_table.column("Data intrare", anchor=CENTER, width=100)
        self.sam_table.column("Data iesire", anchor=CENTER, width=100)
        self.sam_table.column("Durata parcare", anchor=CENTER, width=100)
        self.sam_table.column("Status", anchor=CENTER, width=100)

        self.sam_table.heading("#0", text="ID Rezervare", anchor=CENTER)
        self.sam_table.heading("Nr Auto", text="Nr Auto", anchor=CENTER)
        self.sam_table.heading("Transportator", text="Transportator", anchor=CENTER)
        self.sam_table.heading("Nume sofer", text="Nume sofer", anchor=CENTER)
        self.sam_table.heading("Prenume sofer", text="Prenume sofer", anchor=CENTER)
        self.sam_table.heading("Sigiliu", text="Sigiliu", anchor=CENTER)
        self.sam_table.heading("Data intrare", text="Data intrare", anchor=CENTER)
        self.sam_table.heading("Data iesire", text="Data iesire", anchor=CENTER)
        self.sam_table.heading("Durata parcare", text="Durata parcare", anchor=CENTER)
        self.sam_table.heading("Status", text="Status", anchor=CENTER)

        self.sam_table.pack()
        self.load_samsung()


        # Frame vizitatori - facem interfata

        self.logo_vizitatori_frame = Frame(self.vizitatori_frame)
        self.logo_vizitatori_frame.pack()

        self.logo_vizitatori_title = Label(self.logo_vizitatori_frame, text = "Intrari / iesiri vizitatori Tauros", font=("Arial", 20))
        self.logo_vizitatori_title.pack()

        self.visit_frame = Frame(self.vizitatori_frame)
        self.visit_frame.pack(pady=10)

        self.visit_plate_label = Label(self.visit_frame, text="Nr Auto:")
        self.visit_plate_label.grid(row=0, column=0, padx=5, sticky="w")

        self.visit_plate_entry = Entry(self.visit_frame, width=23, state="readonly")
        self.visit_plate_entry.grid(row=0, column=1, padx=5, sticky="w")

        self.visit_nume_label = Label(self.visit_frame, text="Nume:")
        self.visit_nume_label.grid(row=0, column=2, padx=5, sticky="w")

        self.visit_nume_entry = Entry(self.visit_frame, width=23, state="readonly")
        self.visit_nume_entry.grid(row=0, column=3, padx=5, sticky="w")

        self.visit_id_label = Label(self.visit_frame, text="Firma:")
        self.visit_id_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.visit_id_entry = Entry(self.visit_frame, width=23, state="readonly")
        self.visit_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.visit_destinatie_label = Label(self.visit_frame, text="Departament:")
        self.visit_destinatie_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.visit_destinatie_entry = Entry(self.visit_frame, width=23, state="readonly")
        self.visit_destinatie_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.visit_in_date = Label(self.visit_frame, text="Data intrare:")
        self.visit_in_date.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.visit_in_date_entry = DateEntry(self.visit_frame, locale='ro_RO', date_pattern='yyyy-MM-dd')
        self.visit_in_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # print(self.visit_in_date_entry.get())

        self.visit_time_in_label = Label(self.visit_frame, text=f"Ora intrare:")
        self.visit_time_in_label.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        self.visit_time_in_entry = Entry(self.visit_frame, width=23, state="readonly")
        self.visit_time_in_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        self.visit_time_in_but = Button(self.visit_frame, text="Preia ora", command=lambda:self.cur_time("in"))
        self.visit_time_in_but.grid(row=2, column=4, padx=5, pady=5, sticky="w")

        self.visit_out_date = Label(self.visit_frame, text="Data iesire:")
        self.visit_out_date.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.visit_out_date_entry = DateEntry(self.visit_frame, locale='ro_RO', date_pattern='yyyy-MM-dd', state="readonly")
        self.visit_out_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.visit_time_out_label = Label(self.visit_frame, text=f"Ora iesire:")
        self.visit_time_out_label.grid(row=3, column=2, padx=5, pady=5, sticky="w")

        self.visit_time_out_entry = Entry(self.visit_frame, width=23, state="readonly")
        self.visit_time_out_entry.grid(row=3, column=3, padx=5, pady=5, sticky="w")

        self.visit_time_out_but = Button(self.visit_frame, text="Preia ora", command=lambda:self.cur_time("out"), state="disabled")
        self.visit_time_out_but.grid(row=3, column=4, padx=5, pady=5, sticky="w")

        self.visit_status_label = Label(self.visit_frame, text="Status:")
        self.visit_status_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.visit_status = Label(self.visit_frame, text="INREGISTRARE", fg="red")
        self.visit_status.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        self.visit_lpr_id_label = Label(self.visit_frame, text="LPR ID:")
        self.visit_lpr_id_label.grid(row=4, column=2, padx=5, pady=5, sticky="w")

        self.visit_lpr_id = Label(self.visit_frame, text="")
        self.visit_lpr_id.grid(row=4, column=3, padx=5, pady=5, sticky="w")

        # print(type(self.visit_status.cget("text")))

        # Frame-ul cu butoane pentru vizitatori

        self.visit_butt_frame = Frame(self.vizitatori_frame)
        self.visit_butt_frame.pack(pady=10)

        self.visit_save_button = Button(self.visit_butt_frame, text="Salveaza", command=self.tauros_visit_save, state=DISABLED)
        self.visit_save_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.visit_delete_button = Button(self.visit_butt_frame, text="Sterge", command=self.clear_visit)
        self.visit_delete_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.visit_update_button = Button(self.visit_butt_frame, text="Actualizeaza", state="disabled", command=self.update_visitor)
        self.visit_update_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.visit_new_button = Button(self.visit_butt_frame, text="Adaugare Manual", command=self.new_visitor)
        self.visit_new_button.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Frame-ul cu treeview pentru vizitatori

        self.visit_tree_frame = Frame(self.vizitatori_frame)
        self.visit_tree_frame.pack(pady=10)

        self.visit_tree = ttk.Treeview(self.visit_tree_frame)
        self.visit_tree["columns"] = ("Nr Auto", "Nume", "Firma", "Departament", "Data Intrare", "Ora Intrare", "Data Iesire", "Ora Iesire", "Status")
        self.visit_tree.column("#0", width=0, stretch=NO)
        self.visit_tree.column("Nr Auto", anchor=CENTER, width=100)
        self.visit_tree.column("Nume", anchor=CENTER, width=100)
        self.visit_tree.column("Firma", anchor=CENTER, width=100)
        self.visit_tree.column("Departament", anchor=CENTER, width=100)
        self.visit_tree.column("Data Intrare", anchor=CENTER, width=100)
        self.visit_tree.column("Ora Intrare", anchor=CENTER, width=100)
        self.visit_tree.column("Data Iesire", anchor=CENTER, width=100)
        self.visit_tree.column("Ora Iesire", anchor=CENTER, width=100)
        self.visit_tree.column("Status", anchor=CENTER, width=100)

        self.visit_tree.heading("#0", text="", anchor=CENTER)
        self.visit_tree.heading("Nr Auto", text="Nr Auto", anchor=CENTER)
        self.visit_tree.heading("Nume", text="Nume", anchor=CENTER)
        self.visit_tree.heading("Firma", text="Firma", anchor=CENTER)
        self.visit_tree.heading("Departament", text="Departament", anchor=CENTER)
        self.visit_tree.heading("Data Intrare", text="Data Intrare", anchor=CENTER)
        self.visit_tree.heading("Ora Intrare", text="Ora Intrare", anchor=CENTER)
        self.visit_tree.heading("Data Iesire", text="Data Iesire", anchor=CENTER)
        self.visit_tree.heading("Ora Iesire", text="Ora Iesire", anchor=CENTER)
        self.visit_tree.heading("Status", text="Status", anchor=CENTER)

        self.visit_tree.pack()

        self.visit_tree.bind("<Double-1>", self.select_visitor)
        self.visit_tree.bind("<Return>", self.select_visitor)

        self.load_visitors()
        

    # cautare cap tractor in lista
    def search_auto(self):
        global truck_plate
        self.query = self.nr_auto_combo.get()
        if self.query:
            # Perform search based on the query and update the combobox options
            filtered_values = [value for value in self.truck_plate if self.query.lower() in value.lower()]
            self.nr_auto_combo['values'] = filtered_values
        else:
            self.nr_auto_combo['values'] = self.truck_plate
    # cautare remorca in lista
    def search_remorca(self):
        # try:
        #     self.tms_db = mysql.connector.connect(
        #         host = os.getenv("HOST"),
        #         user = os.getenv("USER"),
        #         passwd = os.getenv("PASS"),
        #         database = os.getenv("DB"),
        #         auth_plugin='mysql_native_password'
        #     )
        # except:
        #     print("Could not connect to MySQL")
        #     mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server")
        #     quit()
        # # Generam un nou cursor
        # self.my_cursor1 = self.tms_db.cursor()
        # # self.my_cursor1.execute("SELECT plate_id, plate_no, status FROM lpr_cam WHERE status= 'CHECK'")
        # Selectam remorcile din tabel. 
        cursor.execute("SELECT plate_no FROM tauros_truck WHERE categorie='SEMIREMORCA'")
        self.nr_auto_remorca = cursor.fetchall()
        # cursor.close()
        # connection.close()
        remorca_plate = []
        for remorca in self.nr_auto_remorca:
            remorca_plate.append(remorca[0])
        # global nr_auto_cap
        self.query = self.remorca_combo.get()
        if self.query:
            # Perform search based on the query and update the combobox options
            filtered_values = [value for value in remorca_plate if self.query.lower() in value.lower()]
            self.remorca_combo['values'] = filtered_values
        else:
            self.remorca_combo['values'] = remorca_plate

    # VErificare numere auto detectate de LPR.
    def search_lpr(self):
        try:
            self.tms_db = mysql.connector.connect(
                host = os.getenv("HOST"),
                user = os.getenv("USER"),
                passwd = os.getenv("PASS"),
                database = os.getenv("DB"),
                auth_plugin='mysql_native_password'
            )
        except:
            print("Could not connect to MySQL")
            mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server")
            quit()
        # Generam un nou cursor
        # self.my_cursor1 = self.tms_db.cursor()
        # self.my_cursor1.execute("SELECT plate_id, plate_no, status FROM lpr_cam WHERE status= 'CHECK'")
        # self.my_cursor1.execute("SELECT id, cap_tractor, label FROM registru WHERE label='Other' ORDER BY id DESC LIMIT 1")
        # self.my_cursor1.execute("SELECT id, cap_tractor, label, token FROM registru ORDER BY id DESC LIMIT 1")
        cursor.execute("SELECT id, cap_tractor, label, token FROM registru ORDER BY id DESC LIMIT 1")
        self.lpr_values = cursor.fetchall()
        
        # self.my_cursor1.close()
        # self.tms_db.close()
        
        if self.lpr_values:
            print(self.lpr_values)
            for id, plate, status, token in self.lpr_values:
                print(id, plate, status, token)
                self.lpr_input.delete(0, END)
                self.lpr_input.insert(0, plate)

                # Verificam daca este camion Tauros

                if plate in self.truck_plate:
                    tauros_truck = messagebox.showinfo(title="Camion Tauros", message=f"{plate} este camion Tauros")
                    if tauros_truck == "ok":
                        self.main_window.select(0)
                        self.n = plate
                        self.nr_auto_combo.set(self.n)
                        # self.my_cursor1.execute("UPDATE lpr_cam SET status = 'PARKED' WHERE plate_id = %s", (id,))
                        # self.tms_db.commit()

                else:
                    # Verificare token in functie de ce spune camera. 
                    if status == "Other":
                        warning = messagebox.askyesno(title="Neavizat", message="Nr. auto neavizat, vizitator?")
                        print(warning)
                        if warning:
                            self.main_window.select(2)
                            self.clear_visit()
                            self.visit_plate_entry.config(state="normal")
                            self.visit_plate_entry.delete(0, END)
                            self.visit_plate_entry.insert(0, plate)
                            self.visit_plate_entry.config(state="readonly")
                            self.visit_lpr_id.config(text=id)
                            self.visit_status.config(text="INREGISTRARE", fg="red")
                            self.visit_save_button.config(state=NORMAL)
                        else:
                            self.my_cursor1.execute("UPDATE registru SET token = 'DENIED' WHERE id = %s", (id,))
                            self.tms_db.commit()
                            messagebox.showinfo(title="Camion Respins", message="Nr. auto respins, necesar a parasi curtea.")
                        
                    # Verificam daca este camion Samsung si populam campurile. 
                    if status =="Samsung":
                        samsung_truck = messagebox.showinfo(title="Camion Samsung", message=f"{plate} este camion Samsung")
                        if samsung_truck == "ok":
                            # try:
                            #     self.tms_db = mysql.connector.connect(
                            #         host = os.getenv("HOST"),
                            #         user = os.getenv("USER"),
                            #         passwd = os.getenv("PASS"),
                            #         database = os.getenv("DB"),
                            #         auth_plugin='mysql_native_password'
                            #     )
                            # except:
                            #     print("Could not connect to MySQL")
                            #     mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server")
                            #     quit()
                            # self.my_cursor = self.tms_db.cursor()
                            sql = "SELECT * from tauros_park_main WHERE plate_no = %s AND place_status = 'REZERVAT'"
                            values = (plate, )
                            cursor.execute(sql, values)
                            self.result = cursor.fetchall()
                            if self.result:
                                print(self.result)
                                # activam modulul samsung si se completeaza datele.
                                self.main_window.select(1)
                                self.sam_plate_no_entry.config(state="normal")
                                self.sam_plate_no_entry.delete(0, END)
                                self.sam_plate_no_entry.insert(0, plate)
                                self.sam_plate_no_entry.config(state="readonly")
                                self.park_place.config(state="normal")
                                self.park_place.delete(0, END)
                                self.park_place.insert(0, self.result[0][5])
                                self.park_place.config(state="readonly")
                                self.sam_nume_entry.config(state="normal")
                                self.sam_nume_entry.delete(0, END)
                                self.sam_nume_entry.insert(0, self.result[0][3])
                                self.sam_nume_entry.config(state="readonly")
                                self.sam_prenume_entry.config(state="normal")
                                self.sam_prenume_entry.delete(0, END)
                                self.sam_prenume_entry.insert(0, self.result[0][4])
                                self.sam_prenume_entry.config(state="readonly")
                                self.sam_seal_entry.config(state="normal")
                                self.sam_id_label.config(text=f"ID: {self.result[0][0]}")
                                self.sam_save_button.config(state=NORMAL)
                            # self.my_cursor.close()
                            # self.tms_db.close()

                    self.lpr_input.delete(0, END)
        else:
            messagebox.showinfo(title="Negasit", message="Nu s-a citit nici un numar auto!")

    
    def cur_time(self, direction):
        self.current_time = time.strftime("%H:%M:%S")
        if direction == "in":            
            self.visit_time_in_entry.config(state="normal")
            self.visit_time_in_entry.delete(0, END)
            self.visit_time_in_entry.insert(0, self.current_time)
            self.visit_time_in_entry.config(state="readonly")

        elif direction == "out":
            self.visit_time_out_entry.config(state="normal")
            self.visit_time_out_entry.delete(0, END)
            self.visit_time_out_entry.insert(0, self.current_time)
            self.visit_time_out_entry.config(state="readonly")

    # Inregistram masina in treeview si baza de date.
    def tauros_visit_save(self):
        try:
            self.tms_db = mysql.connector.connect(
                host = os.getenv("HOST"),
                user = os.getenv("USER"),
                passwd = os.getenv("PASS"),
                database = os.getenv("DB"),
                auth_plugin='mysql_native_password'
            )
        except:
            print("Could not connect to MySQL")
            mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server")
            quit()
        global visit_manual
        self.my_cursor = self.tms_db.cursor()
        self.visit_save_button.config(state=DISABLED)
        self.visit_status.config(text="PARCAT", fg="green")
        lpr_id_value = ""

        if self.visit_manual == False:
            lpr_id_value = int(self.visit_lpr_id.cget("text"))
            self.my_cursor.execute("UPDATE registru SET token = 'PARKED' WHERE id = %s", (self.visit_lpr_id.cget("text"),))
            self.tms_db.commit()
            # self.my_cursor.execute("UPDATE lpr_cam SET Date_In = %s WHERE plate_id = %s", (self.visit_in_date_entry.get(), self.visit_lpr_id.cget("text")))
            self.tms_db.commit()
            self.visit_tree.insert(parent='', index='end', iid=lpr_id_value, text="", values=(self.visit_plate_entry.get(), \
                                                                                                                self.visit_nume_entry.get(), \
                                                                                                                self.visit_id_entry.get(), \
                                                                                                                self.visit_destinatie_entry.get(), \
                                                                                                                self.visit_in_date_entry.get(), \
                                                                                                                self.visit_time_in_entry.get(), \
                                                                                                                "IN CURTE", \
                                                                                                                self.visit_time_out_entry.get(), \
                                                                                                                self.visit_status.cget("text")))
        
        else:
            self.my_cursor.execute("INSERT INTO lpr_cam (plate_no, status, Date_In) VALUES (%s, %s, %s)", (self.visit_plate_entry.get(), "PARKED", self.visit_in_date_entry.get()))
            self.tms_db.commit()
            self.my_cursor.execute("SELECT * FROM lpr_cam ORDER BY plate_id DESC LIMIT 1")
            self.result = self.my_cursor.fetchone()
            print(self.result[0])
            lpr_id_value = int(self.result[0])
            self.visit_tree.insert(parent='', index='end', iid=int(self.result[0]), text="", values=(self.visit_plate_entry.get(), \
                                                                                                                self.visit_nume_entry.get(), \
                                                                                                                self.visit_id_entry.get(), \
                                                                                                                self.visit_destinatie_entry.get(), \
                                                                                                                self.visit_in_date_entry.get(), \
                                                                                                                self.visit_time_in_entry.get(), \
                                                                                                                "IN CURTE", \
                                                                                                                self.visit_time_out_entry.get(), \
                                                                                                                self.visit_status.cget("text")))

        # TO DO

        
        
        # if self.visit_manual == False:
        #     self.my_cursor.execute("UPDATE lpr_cam SET status = 'PARKED' WHERE plate_id = %s", (self.visit_lpr_id.cget("text"),))
        #     self.tms_db.commit()
        #     self.my_cursor.execute("UPDATE lpr_cam SET Date_In = %s WHERE plate_id = %s", (self.visit_in_date_entry.get(), self.visit_lpr_id.cget("text")))
        #     self.tms_db.commit()
        
        # else:
        #     self.my_cursor.execute("INSERT INTO lpr_cam (plate_no, status, Date_In) VALUES (%s, %s, %s)", (self.visit_plate_entry.get(), "PARKED", self.visit_in_date_entry.get()))
        #     self.tms_db.commit()
        sql = "INSERT INTO reg_visit (nr_auto, nume, buletin, dept, data_in, ora_in, visit_status, create_date, lpr_id) VALUES \
            (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (self.visit_plate_entry.get(),
                self.visit_nume_entry.get(),
                self.visit_id_entry.get(),
                self.visit_destinatie_entry.get(),
                self.visit_in_date_entry.get(),
                self.visit_time_in_entry.get(),
                self.visit_status.cget("text"),
                self.visit_in_date_entry.get(),
                lpr_id_value)
        
        self.my_cursor.execute(sql, val)
        self.tms_db.commit()
        self.my_cursor.close()
        self.tms_db.close()
        self.visit_tree.after(3000, self.clear_visit)            

    # Se golesc si reseteaza campurile
    def clear_visit(self):
        self.visit_plate_entry.config(state="normal")
        self.visit_plate_entry.delete(0, END)
        self.visit_nume_entry.config(state="normal")
        self.visit_nume_entry.delete(0, END)
        self.visit_id_entry.config(state="normal")
        self.visit_id_entry.delete(0, END)
        self.visit_destinatie_entry.config(state="normal")
        self.visit_destinatie_entry.delete(0, END)
        self.visit_time_in_entry.config(state="normal")
        self.visit_time_in_entry.delete(0, END)
        self.visit_time_in_entry.config(state="readonly")
        self.visit_time_out_entry.config(state="normal")
        self.visit_time_out_entry.delete(0, END)
        self.visit_time_out_entry.config(state="readonly")
        self.visit_status.config(text="INREGISTARE", fg="red")
        self.visit_in_date_entry.grid_forget()
        self.visit_in_date_entry = DateEntry(self.visit_frame, locale='ro_RO', date_pattern='yyyy-MM-dd')
        self.visit_in_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.visit_in_date_entry.delete(0, END)
        self.visit_out_date_entry.grid_forget()
        self.visit_out_date_entry = DateEntry(self.visit_frame, locale='ro_RO', date_pattern='yyyy-MM-dd', state="readonly")
        self.visit_out_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.visit_out_date_entry.delete(0, END)
        self.visit_save_button.config(state=DISABLED)
        self.visit_delete_button.config(state=NORMAL)
        self.visit_lpr_id.config(text="")
        self.visit_time_in_but.config(state=NORMAL)
        self.visit_time_out_but.config(state=DISABLED)

    
    def select_visitor(self, e):
        self.clear_visit()
        self.selected = self.visit_tree.focus()
        self.values = self.visit_tree.item(self.selected, 'values')
        if len(self.values) != 0:
            self.visit_lpr_id.config(text = self.selected)
            self.visit_plate_entry.insert(0, self.values[0])
            self.visit_plate_entry.config(state="readonly")
            self.visit_nume_entry.insert(0, self.values[1])
            self.visit_nume_entry.config(state="readonly")
            self.visit_id_entry.insert(0, self.values[2])
            self.visit_id_entry.config(state="readonly")
            self.visit_destinatie_entry.insert(0, self.values[3])
            self.visit_destinatie_entry.config(state="readonly")
            # self.visit_in_date_entry.insert(0, self.values[4])
            # self.visit_in_date_entry.config(state="readonly")
            self.visit_in_date_entry.grid_forget()
            self.visit_in_date_entry = Label(self.visit_frame, text=self.values[4])
            self.visit_in_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
            self.visit_time_in_entry.config(state="normal")
            self.visit_time_in_entry.insert(0, self.values[5])
            self.visit_time_in_entry.config(state="readonly")
            self.visit_time_out_entry.config(state="normal")
            self.visit_time_out_entry.insert(0, self.values[7])
            self.visit_time_out_entry.config(state="readonly")
            self.visit_status.config(text=self.values[8], fg="green")
            self.visit_time_in_but.config(state="disabled")
            if self.values[8] == "IESIT":
                self.visit_time_out_but.config(state="disabled")
                self.visit_out_date_entry.grid_forget()
                self.visit_out_date_entry = Label(self.visit_frame, text=self.values[6])
                self.visit_out_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
                self.visit_update_button.config(state="disabled")
            else:
                self.visit_time_out_but.config(state="normal")
                self.visit_update_button.config(state="normal")
            self.visit_save_button.config(state="disabled")
            self.visit_delete_button.config(state="disabled")

    # Functia de actualizare a vizitatorilor
    def update_visitor(self):
        try:
            self.tms_db = mysql.connector.connect(
                host = os.getenv("HOST"),
                user = os.getenv("USER"),
                passwd = os.getenv("PASS"),
                database = os.getenv("DB"),
                auth_plugin='mysql_native_password'
            )
        except:
            print("Could not connect to MySQL")
            mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server")
            quit()
        self.my_cursor = self.tms_db.cursor()
        self.visit_status.config(text="IESIT", fg="blue")
        self.selected = self.visit_tree.focus()
        self.visit_tree.item(self.selected, text="", values=(self.visit_plate_entry.get(), \
                                                            self.visit_nume_entry.get(), \
                                                            self.visit_id_entry.get(), \
                                                            self.visit_destinatie_entry.get(), \
                                                            self.visit_in_date_entry.cget("text"), \
                                                            self.visit_time_in_entry.get(), \
                                                            self.visit_out_date_entry.get(), \
                                                            self.visit_time_out_entry.get(), \
                                                            self.visit_status.cget("text")))
        
        sql = "UPDATE reg_visit SET data_out = %s, ora_out = %s, visit_status = %s WHERE lpr_id = %s"
        values = (self.visit_out_date_entry.get(), self.visit_time_out_entry.get(), self.visit_status.cget("text"), self.visit_lpr_id.cget("text"))
        self.my_cursor.execute(sql, values)
        self.tms_db.commit()

        sql = "UPDATE lpr_cam SET status = 'EXITED', date_out = %s WHERE plate_id = %s"
        values = (self.visit_out_date_entry.get(), self.visit_lpr_id.cget("text"))
        self.my_cursor.execute(sql, values)
        self.tms_db.commit()
        self.visit_in_date_entry.grid_forget()
        self.visit_in_date_entry = DateEntry(self.visit_frame, locale='ro_RO', date_pattern='yyyy-MM-dd')
        self.visit_in_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.my_cursor.close()
        self.tms_db.close()
        self.visit_tree.after(3000, self.clear_visit)


    # Incarcam inregistrarile din baza de date la pornirea programului
    def load_visitors(self):
        try:
            self.tms_db = mysql.connector.connect(
                host = os.getenv("HOST"),
                user = os.getenv("USER"),
                passwd = os.getenv("PASS"),
                database = os.getenv("DB"),
                auth_plugin='mysql_native_password'
            )
        except:
            print("Could not connect to MySQL")
            mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server")
            quit()
        self.my_cursor = self.tms_db.cursor()
        sql = "SELECT * FROM reg_visit"
        self.my_cursor.execute(sql)
        records = self.my_cursor.fetchall()
        for i in records:
            self.visit_tree.insert(parent='', index='end', iid=i[11], text="", values=(i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]))
        self.my_cursor.close()
        self.tms_db.close()


    # Incarcam inregistrarile din baza de date pentru samsung la pornirea programului
    def load_samsung(self):
        try:
            self.tms_db = mysql.connector.connect(
                host = os.getenv("HOST"),
                user = os.getenv("USER"),
                passwd = os.getenv("PASS"),
                database = os.getenv("DB"),
                auth_plugin='mysql_native_password'
            )
        except:
            print("Could not connect to MySQL")
            mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server")
            quit()
        self.my_cursor = self.tms_db.cursor()
        sql = "SELECT * FROM tauros_park_main"
        self.my_cursor.execute(sql)
        records = self.my_cursor.fetchall()
        for i in records:
            print(i)
            self.sam_table.insert(parent='', index='end', iid=i[0], text=i[0], values=(i[2], i[5], i[3], i[4], i[8], i[6], i[7], i[9], i[1]))
        self.my_cursor.close()
        self.tms_db.close()
    
    def new_visitor(self):
        global visit_manual
        self.visit_manual = True
        self.clear_visit()
        self.visit_save_button.config(state="normal")

    def samsung_save(self):
        column = self.sam_table.focus(34)
        self.sam_table.selection_set(34)
        values = self.sam_table.item(34, 'values')
        print(f"Valori: {values}")


# Testam aplicatia

if __name__ == "__main__":
    root = Tk()
    root.title("Registru parcare")
    registru = Registru_parcare(root)
    root.mainloop()



        

