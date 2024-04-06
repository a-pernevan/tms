from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from classes.add_vehicle import Vehicule
import mysql.connector
import os
from dotenv import load_dotenv

class Clients:
    def __init__(self, root):
        self.main_window = ttk.Notebook(root)
        self.main_window.pack(pady=0)

        load_dotenv()
        
        self.main_frame = Frame(self.main_window, width=900, height=600)
        self.client_frame = Frame(self.main_window, width=900, height=600)

        self.main_frame.pack(fill=BOTH, expand=1)
        self.client_frame.pack(fill=BOTH, expand=1)

        self.main_window.add(self.main_frame, text="Principal")
        self.main_window.add(self.client_frame, text="Gestionare firme")
        self.adaugare_cam = Button(self.main_frame, text="Adaugare", command=self.show_clients)
        self.adaugare_cam.pack()

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
        self.my_cursor.execute("SELECT * FROM clienti")
        print (self.my_cursor.fetchall())
        

