from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import os
from dotenv import load_dotenv

class Registru_parcare:
    def __init__(self, master):
        super().__init__()
        load_dotenv()

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
        self.nr_auto_cap = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "Yusen"]
        self.nr_auto_remorca = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "Yusen"]

        # Cream interfata si notebook-ul
        # self.master = master
        # self.master.title("Registru parcare")
        self.main_window = ttk.Notebook(master, width=900, height=600)
        self.main_window.pack(pady=0)

        self.tauros_frame = Frame(self.main_window)
        self.tauros_frame.pack(fill=BOTH, expand=1, anchor=W)

        self.samsung_frame = Frame(self.main_window)
        self.samsung_frame.pack(fill=BOTH, expand=1, anchor=W)

        self.vizitatori_frame = Frame(self.main_window)
        self.vizitatori_frame.pack(fill=BOTH, expand=1, anchor=W)

        self.main_window.add(self.tauros_frame, text="Tauros")
        self.main_window.add(self.samsung_frame, text="Samsung")
        self.main_window.add(self.vizitatori_frame, text="Vizitatori")

        self.logo_frame = Frame(self.tauros_frame)
        self.logo_frame.pack()

        self.logo_title = Label(self.logo_frame, text="Intrari / Iesiri Tauros", font=("Arial", 20))
        self.logo_title.pack()

        self.truck_frame = Frame(self.tauros_frame)
        self.truck_frame.pack(pady=10)

        self.nr_auto_label = Label(self.truck_frame, text="Nr auto:")
        self.nr_auto_label.grid(row=0, column=0, padx=5)

        self.remorca_label = Label(self.truck_frame, text="Remorca:")
        self.remorca_label.grid(row=0, column=2, padx=5)

        self.nr_auto_combo = ttk.Combobox(self.truck_frame, postcommand=self.search_auto)
        self.nr_auto_combo.grid(row=0, column=1)

        self.remorca_combo = ttk.Combobox(self.truck_frame, postcommand=self.search_remorca)
        self.remorca_combo.grid(row=0, column=3)

        self.lpr_label = Label(self.truck_frame, text="LPR:")
        self.lpr_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.lpr_input = Entry(self.truck_frame, width=23)
        self.lpr_input.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.test_button = Button(self.truck_frame, text="Verifica nr auto", command=self.search_lpr)
        self.test_button.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # self.test_button = Button(self.tauros_frame, text="Test")
        # self.test_button.grid(row=0, column=0)

        # cautare cap tractor
    def search_auto(self):
        # global nr_auto_cap
        self.query = self.nr_auto_combo.get()
        if self.query:
            # Perform search based on the query and update the combobox options
            filtered_values = [value for value in self.nr_auto_cap if self.query.lower() in value.lower()]
            self.nr_auto_combo['values'] = filtered_values
        else:
            self.nr_auto_combo['values'] = self.nr_auto_cap


    def search_remorca(self):
        # global nr_auto_cap
        self.query = self.remorca_combo.get()
        if self.query:
            # Perform search based on the query and update the combobox options
            filtered_values = [value for value in self.nr_auto_remorca if self.query.lower() in value.lower()]
            self.remorca_combo['values'] = filtered_values
        else:
            self.remorca_combo['values'] = self.nr_auto_remorca

    def search_lpr(self):
        self.my_cursor.execute("SELECT plate_no, status FROM lpr_cam WHERE status= 'CHECK'")
        self.lpr_values = self.my_cursor.fetchall()
        print(self.lpr_values)
        for plate, status in self.lpr_values:
            print(plate, status)
            self.lpr_input.delete(0, END)
            self.lpr_input.insert(0, plate)
            if plate in self.nr_auto_cap:
                tauros_truck = messagebox.showinfo(title="Camion Tauros", message="Nr. auto disponibil")
                if tauros_truck == "ok":
                    self.main_window.select(0)
            else:
                warning = messagebox.askyesno(title="Neavizat", message="Nr. auto neavizat, vizitator?")
                print(warning)
                if warning:
                    self.main_window.select(2)
                else:
                    self.my_cursor.execute("UPDATE lpr_cam SET status = 'DENIED' WHERE plate_no = %s", (plate,))
                    self.tms_db.commit()
                    messagebox.showinfo(title="Camion Respins", message="Nr. auto respins, necesar a parasi curtea.")
        


# Testam aplicatia

if __name__ == "__main__":
    root = Tk()
    root.title("Registru parcare")
    registru = Registru_parcare(root)
    root.mainloop()



        

