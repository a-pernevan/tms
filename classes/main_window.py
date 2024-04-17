from site import ENABLE_USER_SITE
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
# from tkinter import NoteBook
from angajati import Angajati_firma
import mysql.connector
import os
from dotenv import load_dotenv

class Main_Window:
    def __init__(self, root):
        self.main_window = ttk.Notebook(root, width=900, height=600)
        self.main_window.pack(pady=0)

        

        load_dotenv()
        
        # self.main_frame = Frame(self.main_window)
        # self.client_frame = Frame(self.main_window)
        self.main_frame = Frame(self.main_window, width=900, height=600)
        # self.client_frame = Frame(self.main_window, width=900, height=600)
        # self.angajat_frame = Frame(self.main_window, width=900, height=600)

        self.main_frame.pack(fill=BOTH, expand=1, anchor=W)
        # self.client_frame.pack(fill=BOTH, expand=1, anchor=W)
        # self.angajat_frame.pack(fill=BOTH, expand=1, anchor=W)

        self.main_window.add(self.main_frame, text="Principal")
        # self.main_window.add(self.client_frame, text="Gestionare firme")
        # self.main_window.add(self.angajat_frame, text="Gestionare angajati")

        self.adaugare_cam = Button(self.main_frame, text="Afisare firme", command=self.show_clients)
        self.adaugare_cam.grid(row=0, column=0)

        self.angajati_button = Button(self.main_frame, text="Gestionare angajati", command=self.admin_angajati)
        self.angajati_button.grid(row=1, column=0, pady=5)



        # self.main_window.hide(1)
        # self.main_window.hide(2)

        # Create connection to database
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
            self,mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server")
            quit()
        self.my_cursor = self.tms_db.cursor()

    def show_clients(self):
        self.client_frame = Frame(self.main_window, width=900, height=600)
        self.main_window.add(self.client_frame, text="Gestionare firme")
        self.main_window.select(1)
        self.show_client_frame = LabelFrame(self.client_frame, text= "Afisare clienti", width=800, height=700)
        self.show_client_frame.grid(row=0, column=0, sticky="nw")
        self.close = Button(self.show_client_frame, text="inchidere", command=lambda:self.main_window.hide(1))
        self.close.grid(row=0, column=0)
        self.list_clients()
        # self.list_all = ttk.Treeview(self.client_frame)
        # # self.list_all["columns"] = 

    def list_clients(self):
        self.my_cursor.execute("SELECT * FROM clienti")
        self.result = self.my_cursor.fetchall()
        print(self.result)
        for index, x in enumerate(self.result):
            print(index)
            print(x[1])
            index += 1
            y = 0
            self.client_name = Label(self.show_client_frame, text=x[1]).grid(row=index, column=y, sticky="nw")
            y += 1

        
    def admin_angajati(self):
        # cream un frame nou un notebook
        self.angajat_frame = Frame(self.main_window, width=900, height=600)
        # Il adaugam la notebook
        self.main_window.add(self.angajat_frame, text="Gestionare angajati")
        # il selectam
        self.main_window.select(self.angajat_frame)
        # Cream un frame nou
        self.modul_angajati_frame = Frame(self.angajat_frame)
        self.modul_angajati_frame.pack(fill=BOTH, expand=1, anchor=W)
        # initializam clasa angajati_firma
        self.create_frame = Angajati_firma(self.modul_angajati_frame)
        self.angajati_button.configure(state=DISABLED)
        self.inchide_angajati_button = Button(self.modul_angajati_frame, text="inchidere", command=lambda:(self.main_window.forget(self.main_window.index(self.angajat_frame)), self.angajati_button.configure(state=NORMAL)))
        self.inchide_angajati_button.grid(row=1, column=0)
        

if __name__ == "__main__":
    root = Tk()
    clients = Main_Window(root)
    root.mainloop()
        

