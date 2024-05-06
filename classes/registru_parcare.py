from calendar import c
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# from tkinter.tix import COLUMN
import mysql.connector
import os
from dotenv import load_dotenv
from tkcalendar import DateEntry
import time

class Registru_parcare:
    def __init__(self, master):
        super().__init__()
        load_dotenv()
        
        #Deschidem conexiunea cu baza de date
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

        # Valori demo pt nr camion
        self.nr_auto_cap = ["IS04GCI", "Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "Yusen"]
        self.nr_auto_remorca = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "Yusen"]

        # Cream interfata si notebook-ul
        # self.master = master
        # self.master.title("Registru parcare")
        self.main_window = ttk.Notebook(master, width=900, height=600)
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

        # self.nr_auto_combo = ttk.Combobox(self.truck_frame, postcommand=self.search_auto)
        # self.nr_auto_combo.grid(row=0, column=1)

        self.nr_auto_entry = Entry(self.truck_frame, width=23)
        self.nr_auto_entry.grid(row=0, column=1, padx=5, sticky="w")

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

        # Frame vizitatori - facem interfata

        self.logo_vizitatori_frame = Frame(self.vizitatori_frame)
        self.logo_vizitatori_frame.pack()

        self.logo_vizitatori_title = Label(self.logo_vizitatori_frame, text = "Intrari / iesiri vizitatori Tauros", font=("Arial", 20))
        self.logo_vizitatori_title.pack()

        self.visit_frame = Frame(self.vizitatori_frame)
        self.visit_frame.pack(pady=10)

        self.visit_plate_label = Label(self.visit_frame, text="Nr Auto:")
        self.visit_plate_label.grid(row=0, column=0, padx=5)

        self.visit_plate_entry = Entry(self.visit_frame, width=23)
        self.visit_plate_entry.grid(row=0, column=1, padx=5, sticky="w")

        self.visit_nume_label = Label(self.visit_frame, text="Nume:")
        self.visit_nume_label.grid(row=0, column=2, padx=5, sticky="w")

        self.visit_nume_entry = Entry(self.visit_frame, width=23)
        self.visit_nume_entry.grid(row=0, column=3, padx=5, sticky="w")

        self.visit_id_label = Label(self.visit_frame, text="Buletin:")
        self.visit_id_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.visit_id_entry = Entry(self.visit_frame, width=23)
        self.visit_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.visit_destinatie_label = Label(self.visit_frame, text="Departament:")
        self.visit_destinatie_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.visit_destinatie_entry = Entry(self.visit_frame, width=23)
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

        # Frame-ul cu butoane

        self.visit_butt_frame = Frame(self.vizitatori_frame)
        self.visit_butt_frame.pack(pady=10)

        self.visit_save_button = Button(self.visit_butt_frame, text="Salveaza", command=self.tauros_visit_save)
        self.visit_save_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.visit_delete_button = Button(self.visit_butt_frame, text="Sterge")
        self.visit_delete_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.visit_update_button = Button(self.visit_butt_frame, text="Actualizeaza", state="disabled")
        self.visit_update_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Frame-ul cu treeview

        self.visit_tree_frame = Frame(self.vizitatori_frame)
        self.visit_tree_frame.pack(pady=10)

        self.visit_tree = ttk.Treeview(self.visit_tree_frame)
        self.visit_tree["columns"] = ("Nr Auto", "Nume", "Buletin", "Departament", "Data Intrare", "Ora Intrare", "Data Iesire", "Ora Iesire", "Status")
        self.visit_tree.column("#0", width=0, stretch=NO)
        self.visit_tree.column("Nr Auto", anchor=CENTER, width=100)
        self.visit_tree.column("Nume", anchor=CENTER, width=100)
        self.visit_tree.column("Buletin", anchor=CENTER, width=100)
        self.visit_tree.column("Departament", anchor=CENTER, width=100)
        self.visit_tree.column("Data Intrare", anchor=CENTER, width=100)
        self.visit_tree.column("Ora Intrare", anchor=CENTER, width=100)
        self.visit_tree.column("Data Iesire", anchor=CENTER, width=100)
        self.visit_tree.column("Ora Iesire", anchor=CENTER, width=100)
        self.visit_tree.column("Status", anchor=CENTER, width=100)

        self.visit_tree.heading("#0", text="", anchor=CENTER)
        self.visit_tree.heading("Nr Auto", text="Nr Auto", anchor=CENTER)
        self.visit_tree.heading("Nume", text="Nume", anchor=CENTER)
        self.visit_tree.heading("Buletin", text="Buletin", anchor=CENTER)
        self.visit_tree.heading("Departament", text="Departament", anchor=CENTER)
        self.visit_tree.heading("Data Intrare", text="Data Intrare", anchor=CENTER)
        self.visit_tree.heading("Ora Intrare", text="Ora Intrare", anchor=CENTER)
        self.visit_tree.heading("Data Iesire", text="Data Iesire", anchor=CENTER)
        self.visit_tree.heading("Ora Iesire", text="Ora Iesire", anchor=CENTER)
        self.visit_tree.heading("Status", text="Status", anchor=CENTER)

        self.visit_tree.pack()
        

    # cautare cap tractor in lista
    def search_auto(self):
        # global nr_auto_cap
        self.query = self.nr_auto_combo.get()
        if self.query:
            # Perform search based on the query and update the combobox options
            filtered_values = [value for value in self.nr_auto_cap if self.query.lower() in value.lower()]
            self.nr_auto_combo['values'] = filtered_values
        else:
            self.nr_auto_combo['values'] = self.nr_auto_cap

    # cautare remorca in lista
    def search_remorca(self):
        # global nr_auto_cap
        self.query = self.remorca_combo.get()
        if self.query:
            # Perform search based on the query and update the combobox options
            filtered_values = [value for value in self.nr_auto_remorca if self.query.lower() in value.lower()]
            self.remorca_combo['values'] = filtered_values
        else:
            self.remorca_combo['values'] = self.nr_auto_remorca

    # VErificare numere auto detectate de LPR.
    def search_lpr(self):
        self.my_cursor.execute("SELECT * FROM lpr_cam WHERE status= 'CHECK'")
        self.lpr_values = self.my_cursor.fetchall()

        if self.lpr_values:
            print(self.lpr_values)
            for id, plate, status in self.lpr_values:
                print(id, plate, status)
                self.lpr_input.delete(0, END)
                self.lpr_input.insert(0, plate)

                # Verificam daca este camion Tauros

                if plate in self.nr_auto_cap:
                    tauros_truck = messagebox.showinfo(title="Camion Tauros", message=f"{plate} este camion Tauros")
                    if tauros_truck == "ok":
                        self.main_window.select(0)
                        self.nr_auto_entry.delete(0, END)
                        self.nr_auto_entry.insert(0, plate)
                        self.my_cursor.execute("UPDATE lpr_cam SET status = 'PARKED' WHERE plate_id = %s", (id,))
                        self.tms_db.commit()

                else:
                    warning = messagebox.askyesno(title="Neavizat", message="Nr. auto neavizat, vizitator?")
                    print(warning)
                    if warning:
                        self.main_window.select(2)
                        self.visit_plate_entry.delete(0, END)
                        self.visit_plate_entry.insert(0, plate)
                        self.visit_lpr_id.config(text=id)
                    else:
                        self.my_cursor.execute("UPDATE lpr_cam SET status = 'DENIED' WHERE plate_id = %s", (id,))
                        self.tms_db.commit()
                        messagebox.showinfo(title="Camion Respins", message="Nr. auto respins, necesar a parasi curtea.")
        
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
        self.visit_save_button.config(state=DISABLED)
        self.visit_status.config(text="PARCAT", fg="green")
        self.visit_tree.insert(parent='', index='end', iid=int(self.visit_lpr_id.cget("text")), text="", values=(self.visit_plate_entry.get(), \
                                                                                                                self.visit_nume_entry.get(), \
                                                                                                                self.visit_id_entry.get(), \
                                                                                                                self.visit_destinatie_entry.get(), \
                                                                                                                self.visit_in_date_entry.get(), \
                                                                                                                self.visit_time_in_entry.get(), \
                                                                                                                "IN CURTE", \
                                                                                                                self.visit_time_out_entry.get(), \
                                                                                                                self.visit_status.cget("text")))

        

# Testam aplicatia

if __name__ == "__main__":
    root = Tk()
    root.title("Registru parcare")
    registru = Registru_parcare(root)
    root.mainloop()



        

