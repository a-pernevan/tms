from calendar import c
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import os
from dotenv import load_dotenv
from tkcalendar import DateEntry
import time
from datetime import datetime

class Rezervare_parcare:
    def __init__(self, master):
        super().__init__()
        load_dotenv()

        self.main_window = Toplevel(master)
        self.main_window.title("Rezervare parcare Samsung")

        self.plate_no_label = Label(self.main_window, text="Numar auto:")
        self.plate_no_label.grid(row=0, column=0, sticky="nw")

        self.plate_no_entry = Entry(self.main_window)
        self.plate_no_entry.grid(row=0, column=1, sticky="nw")

        self.driver_name_label = Label(self.main_window, text="Nume sofer:")
        self.driver_name_label.grid(row=1, column=0, sticky="nw")

        self.driver_name_entry = Entry(self.main_window)
        self.driver_name_entry.grid(row=1, column=1, sticky="nw")

        self.driver_lname_label = Label(self.main_window, text="Prenume sofer:")
        self.driver_lname_label.grid(row=2, column=0, sticky="nw")

        self.driver_lname_entry = Entry(self.main_window)
        self.driver_lname_entry.grid(row=2, column=1, sticky="nw")

        self.company_label = Label(self.main_window, text="Transportator:")
        self.company_label.grid(row=3, column=0, sticky="nw")

        self.company_entry = Entry(self.main_window)
        self.company_entry.grid(row=3, column=1, sticky="nw")

        # self.parking_space_label = Label(self.main_window, text="Loc parcare alocat:")
        # self.parking_space_label.grid(row=4, column=0, sticky="nw")

        # self.parking_space_entry = Entry(self.main_window, state="readonly")
        # self.parking_space_entry.grid(row=4, column=1, sticky="nw")

        # self.select_place_button = Button(self.main_window, text="Selecteaza loc")
        # self.select_place_button.grid(row=4, column=2, sticky="nw")

        self.reservation_date_in_label = Label(self.main_window, text="Data intrare:")
        self.reservation_date_in_label.grid(row=5, column=0, sticky="nw")

        self.reservation_date_in_entry = DateEntry(self.main_window, locale='ro_RO', date_pattern='yyyy-MM-dd')
        self.reservation_date_in_entry.grid(row=5, column=1, sticky="nw")

        self.reservation_date_out_label = Label(self.main_window, text="Data iesire:")
        self.reservation_date_out_label.grid(row=6, column=0, sticky="nw")

        self.reservation_date_out_entry = DateEntry(self.main_window, locale='ro_RO', date_pattern='yyyy-MM-dd')
        self.reservation_date_out_entry.grid(row=6, column=1, sticky="nw")

        self.check_availability_button = Button(self.main_window, text="Verifica disponibilitate", command=self.verifica)
        self.check_availability_button.grid(row=7, column=1, sticky="nw")

        self.reservation_button = Button(self.main_window, text="Rezervare", state="disabled")
        self.reservation_button.grid(row=8, column=1, sticky="nw")

        date_in = self.reservation_date_in_entry.get().split("-")
        date_out = self.reservation_date_out_entry.get().split("-")
        
        date1 = datetime(int(date_in[0]), int(date_in[1]), int(date_in[2]))
        date2 = datetime(int(date_out[0]), int(date_out[1]), int(date_out[2]))
        
    def verifica(self):
        date_in_str = str(self.reservation_date_in_entry.get())
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

        sql = ("SELECT date_out FROM tauros_park_main WHERE date_out > %s")
        values = ((date_in_str, ))

        self.my_cursor.execute(sql, values)
        self.result = self.my_cursor.fetchall()

        if self.result:
            print(len(self.result))
            print(self.result)
            if len(self.result) < 20:
                print(f"Free places: {20 - len(self.result)}")
            else:
                print("Parking full")

        elif not self.result:
            print("Parking empty")

        self.my_cursor.close()
        self.tms_db.close()

        # for index, date in enumerate(self.result):
        #     # print(str(date[0]).split("-"))
        #     rez_date = datetime(int(str(date[0]).split("-")[0]), int(str(date[0]).split("-")[1]), int(str(date[0]).split("-")[2]))
        #     print(f"Place {index}: {rez_date}")
        #     if date2 > rez_date:
        #         print(f"Place {index} is available")




if __name__ == "__main__":
    root = Tk()
    root.title("Registru parcare")
    registru = Rezervare_parcare(root)
    root.mainloop()
