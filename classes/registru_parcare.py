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

        self.nr_auto_label = Label(self.truck_frame, text="Nr auto: ")
        self.nr_auto_label.grid(row=0, column=0)

        self.remorca_label = Label(self.truck_frame, text="Remorca: ")
        self.remorca_label.grid(row=1, column=0)

        self.nr_auto_combo = ttk.Combobox(self.truck_frame, postcommand=self.search_auto)
        self.nr_auto_combo.grid(row=0, column=1)

        self.remorca_combo = ttk.Combobox(self.truck_frame, postcommand=self.search_remorca)
        self.remorca_combo.grid(row=1, column=1)

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

# Testam aplicatia

if __name__ == "__main__":
    root = Tk()
    root.title("Registru parcare")
    registru = Registru_parcare(root)
    root.mainloop()



        
