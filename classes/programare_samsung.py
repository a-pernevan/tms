from calendar import c
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from turtle import st
import mysql.connector
import os
from dotenv import load_dotenv
from tkcalendar import DateEntry
import time
from datetime import datetime, timedelta

class Rezervare_parcare:
    def __init__(self, master):
        super().__init__()
        load_dotenv()

        hours = [
            "00:00",
            "01:00",
            "02:00",
            "03:00",
            "04:00",
            "05:00",
            "06:00",
            "07:00",
            "08:00",
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00",
            "18:00",
            "19:00",
            "20:00",
            "21:00",
            "22:00",
            "23:00",
            "24:00",
        ]

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

        self.reservation_hour_in_label = Label(self.main_window, text="Ora intrare:")
        self.reservation_hour_in_label.grid(row=5, column=2, sticky="nw")

        self.reservation_hour_in_combo = ttk.Combobox(self.main_window, values=hours, width=15)
        self.reservation_hour_in_combo.grid(row=5, column=3, sticky="nw")

        # self.reservation_date_out_label = Label(self.main_window, text="Data iesire:")
        # self.reservation_date_out_label.grid(row=6, column=0, sticky="nw")

        # self.reservation_date_out_entry = DateEntry(self.main_window, locale='ro_RO', date_pattern='yyyy-MM-dd')
        # self.reservation_date_out_entry.grid(row=6, column=1, sticky="nw")

        self.reservation_period_label = Label(self.main_window, text="Durata (ore):")
        self.reservation_period_label.grid(row=6, column=0, sticky="nw")

        self.reservation_period_combo = ttk.Combobox(self.main_window, values=["18", "24", "48"])
        self.reservation_period_combo.current(0)
        self.reservation_period_combo.grid(row=6, column=1, sticky="nw")

        self.check_availability_button = Button(self.main_window, text="Verifica disponibilitate", command=self.print_date)
        self.check_availability_button.grid(row=7, column=1, sticky="nw")

        self.reservation_button = Button(self.main_window, text="Rezervare", state="disabled")
        self.reservation_button.grid(row=8, column=1, sticky="nw")

        date_in = self.reservation_date_in_entry.get().split("-")
        # date_out = self.reservation_date_out_entry.get().split("-")
        
        date1 = datetime(int(date_in[0]), int(date_in[1]), int(date_in[2]))
        # date2 = datetime(int(date_out[0]), int(date_out[1]), int(date_out[2]))
        
    def verifica(self, date_in, date_out):
        date_in_str = str(self.reservation_date_in_entry.get())
        print(date_in)
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

        sql = ("SELECT date_out FROM tauros_park_main WHERE date_out > %s AND place_status <> 'PLECAT'")
        values = ((date_in, ))

        self.my_cursor.execute(sql, values)
        self.result = self.my_cursor.fetchall()

        if self.result:
            print(len(self.result))
            print(self.result)
            if len(self.result) < 20:
                print(f"Free places: {20 - len(self.result)}")
                result = messagebox.askyesno(title="Rezultat", message=f"Locuri libere: {20 - len(self.result)}. Rezervati?")
                if result == True:
                    self.rezervare(date_in, date_out)
            else:
                print("Parking full")
                result = messagebox.showwarning(title="Rezultat", message="Parcarea este plina in data selectata!")

        elif not self.result:
            print("Parking empty")
            result = messagebox.askyesno(title="Rezultat", message="Suficiente locuri de parcare. Rezervati?")
            print(result)
            if result == True:
                self.rezervare(date_in, date_out)
            

        self.my_cursor.close()
        self.tms_db.close()

        # for index, date in enumerate(self.result):
        #     # print(str(date[0]).split("-"))
        #     rez_date = datetime(int(str(date[0]).split("-")[0]), int(str(date[0]).split("-")[1]), int(str(date[0]).split("-")[2]))
        #     print(f"Place {index}: {rez_date}")
        #     if date2 > rez_date:
        #         print(f"Place {index} is available")

    def print_date(self):
        date_entry = self.reservation_date_in_entry.get() + " " + self.reservation_hour_in_combo.get()
        print(date_entry)
        print(type(date_entry))
        dbtime_back = datetime.strptime(date_entry, "%Y-%m-%d %H:%M")
        print(dbtime_back)
        print(type(dbtime_back))

        exit_date = dbtime_back + timedelta(hours=int(self.reservation_period_combo.get()))

        print(exit_date)

        self.verifica(dbtime_back, exit_date)

    # def rezervare(self, date_in, date_out):
    #     try:
    #         self.tms_db = mysql.connector.connect(
    #             host = os.getenv("HOST"),
    #             user = os.getenv("USER"),
    #             passwd = os.getenv("PASS"),
    #             database = os.getenv("DB"),
    #             auth_plugin='mysql_native_password'
    #         )
    #     except:
    #         print("Could not connect to MySQL")
    #         mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server")
    #         quit()

    #     self.my_cursor = self.tms_db.cursor()

    #     place_status = "REZERVAT"
    #     truck_no = self.plate_no_entry.get()
    #     f_name = self.driver_name_entry.get()
    #     l_name = self.driver_lname_entry.get()
    #     company = self.company_entry.get()
    #     date_entry = str(date_in)
    #     date_exit = date_out
    #     self.my_cursor.execute(f"SELECT {truck_no} FROM tauros_park_main WHERE place_status='REZERVAT' AND date_in = {date_entry}")
    #     self.result = self.my_cursor.fetchall()

    #     if self.result:
    #         print(self.result)
    #         messagebox.showinfo(title="Eroare", message="Mai exista o rezervare cu aceste date!")

    #     sql = "INSERT INTO tauros_park_main (place_status, plate_no, d_fname, d_lname, company, date_in, date_out) VALUES \
    #         (%s, %s, %s, %s, %s, %s, %s)"
    #     values = (place_status,
    #               truck_no.upper(),
    #               f_name.upper(),
    #               l_name.upper(),
    #               company.upper(),
    #               date_entry,
    #               date_exit)
        
        # self.my_cursor.execute(sql, values)
        # self.tms_db.commit()
        # self.my_cursor.close()
        # self.tms_db.close()

    def rezervare(self, date_in, date_out):
        def confirm(place_status, truck_no, f_name, l_name, company, date_entry, date_exit, durata):
            try:
                self.tms_db = mysql.connector.connect(
                    host=os.getenv("HOST"),
                    user=os.getenv("USER"),
                    passwd=os.getenv("PASS"),
                    database=os.getenv("DB"),
                    auth_plugin='mysql_native_password'
                )
            except:
                print("Could not connect to MySQL")
                mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server")
                quit()

            self.my_cursor = self.tms_db.cursor()
            sql = "INSERT INTO tauros_park_main (place_status, plate_no, d_fname, d_lname, company, date_in, date_out, durata) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (place_status,
                    truck_no.upper(),
                    f_name.upper(),
                    l_name.upper(),
                    company.upper(),
                    date_entry,
                    date_exit,
                    durata)

            self.my_cursor.execute(sql, values)
            self.tms_db.commit()

            self.my_cursor.close()
            self.tms_db.close()

            messagebox.showinfo(title="Rezervare", message="Rezervarea a fost facuta cu succes!")
            self.make_rezervation.destroy()


        try:
            self.tms_db = mysql.connector.connect(
                host=os.getenv("HOST"),
                user=os.getenv("USER"),
                passwd=os.getenv("PASS"),
                database=os.getenv("DB"),
                auth_plugin='mysql_native_password'
            )
        except:
            print("Could not connect to MySQL")
            mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server")
            quit()

        self.my_cursor = self.tms_db.cursor()

        place_status = "REZERVAT"
        truck_no = self.plate_no_entry.get()
        f_name = self.driver_name_entry.get()
        l_name = self.driver_lname_entry.get()
        company = self.company_entry.get()
        date_entry = str(date_in.strftime("%Y-%m-%d %H:%M"))
        date_exit = date_out.strftime("%Y-%m-%d %H:%M")
        durata = self.reservation_period_combo.get()

        self.my_cursor.execute(
            f"SELECT COUNT(*) FROM tauros_park_main WHERE place_status='REZERVAT' AND plate_no = '{truck_no}' AND date_in = '{date_entry}'"
        )
        count = self.my_cursor.fetchone()[0]
        print(count)

        if count > 0:
            
            messagebox.showinfo(title="Eroare", message="Mai exista o rezervare cu aceste date!")
            return


        self.my_cursor.close()
        self.tms_db.close()
        self.make_rezervation = Toplevel(self.main_window)
        self.make_rezervation.transient(self.main_window)
        self.make_rezervation.grab_set()
        self.make_rezervation.title("Confirmare rezervare")

        self.confirm_info = Label(self.make_rezervation, text="Verificati datele!")
        self.confirm_info.grid(row=0, column=0, padx=10, pady=10)
        rez_plate = Label(self.make_rezervation, text=f"Numar auto: {truck_no}")
        rez_plate.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        rez_nume = Label(self.make_rezervation, text=f"Nume: {f_name}, {l_name}")
        rez_nume.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        rez_company = Label(self.make_rezervation, text=f"Companie: {company}")
        rez_company.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        rez_date_in = Label(self.make_rezervation, text=f"Data intrare: {date_entry}")
        rez_date_in.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        rez_date_out = Label(self.make_rezervation, text=f"Data iesire: {date_exit}")
        rez_date_out.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        btn_confirm = Button(self.make_rezervation, text="Confirmare", command= lambda: confirm(place_status, truck_no, f_name, l_name, company, date_entry, date_exit, durata))
        btn_confirm.grid(row=6, column=0, padx=10, pady=10)


if __name__ == "__main__":
    root = Tk()
    root.title("Registru parcare")
    registru = Rezervare_parcare(root)
    root.mainloop()
