from cProfile import label
import locale
import tkinter as tk
from tkinter import Toplevel, ttk
from PIL import Image, ImageTk
from tkinter import W, Button, filedialog, messagebox
try:
    from database.datab import connection, cursor
except:
    mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server, program will exit")
    quit()
from utils.tooltip import ToolTip
from tkcalendar import DateEntry, Calendar
from datetime import datetime, timedelta, date
from liste import Scadente_auto

class Scadente_directe:
    def __init__(self, master, id_tms, nume, tip, tip_scadenta, data_scadenta):
        self.master = master
        self.id_tms = id_tms
        self.nume = nume
        self.tip = tip
        self.tip_scadenta = tip_scadenta
        self.data_scadenta = data_scadenta

        print(self.id_tms, self.nume, self.tip, self.tip_scadenta, self.data_scadenta)
        
        self.adauga_scadenta()
    def check_denumire(self):
        denumire_scadenta = []
        try:
            connection._open_connection()
            sql = "SELECT nume_scadenta FROM tip_scadente"
            cursor.execute(sql)
            result = cursor.fetchall()
            
        except:
            messagebox.showerror(title="Connection error", message="Could not connect to DB Server, program will exit")
            quit()

        for i in result:
            denumire_scadenta.append(i[0])

        if self.tip_scadenta.upper() not in denumire_scadenta:
            sql = "INSERT INTO tip_scadente (nume_scadenta) VALUES (%s)"
            values = (self.tip_scadenta,)
            cursor.execute(sql, values)
            connection.commit()

        connection.close()
        return True

    def check_scadenta(self):
        try:
            connection._open_connection()
            sql = "SELECT * FROM tabel_scadente WHERE id_tms = %s AND scadenta = %s"
            values = (self.id_tms, self.tip_scadenta)
            cursor.execute(sql, values)
            result = cursor.fetchall()

        except:
            messagebox.showerror(title="Connection error", message="Could not connect to DB Server, program will exit")

        finally:
            
            if result:
                sql = "DELETE FROM tabel_scadente WHERE id_tms = %s AND scadenta = %s"
                values = (self.id_tms, self.tip_scadenta)
                cursor.execute(sql, values)
                connection.commit()
                connection.close()
                return True
            else:
                return True
    
    def adauga_scadenta(self):
        if self.check_denumire() and self.check_scadenta():
            data_inv = datetime.strptime(str(self.data_scadenta), "%Y-%m-%d")
            data_scadenta = data_inv + timedelta(days=20)
            print(data_scadenta)
            # input()
            try:
                connection._open_connection()
                sql = "INSERT INTO tabel_scadente (id_tms, nume, tip, scadenta, data_scadenta) VALUES (%s, %s, %s, %s, %s)"
                values = (self.id_tms, self.nume, self.tip, self.tip_scadenta, data_scadenta)
                cursor.execute(sql, values)
                connection.commit()
            
            except:
                messagebox.showerror(title="Connection error", message="Could not connect to DB Server, program will exit")
                quit()

            finally:
                connection.close()

            messagebox.showinfo(title="Success", message= f"Scadenta {self.nume} - {self.tip_scadenta} adaugata cu succes!")

    

class Scadente:
    def __init__(self, master, id_tms, nume, tip):
        self.master = master
        self.id_tms = id_tms
        self.nume = nume
        self.tip = tip
        self.lista_scadente = []

        connection._open_connection()
        self.main_window()

    def main_window(self):
        # TO DO - de terminat functie stergere scadente

        self.icon_new = Image.open("classes/utils/icons/add-text-icon-15.jpg")
        self.icon_new = self.icon_new.resize((22, 22))
        self.icon_new = ImageTk.PhotoImage(self.icon_new)

        self.icon_delete = Image.open("classes/utils/icons/icon-delete-19.jpg")
        self.icon_delete = self.icon_delete.resize((22, 22))
        self.icon_delete = ImageTk.PhotoImage(self.icon_delete)

        self.icon_modify = Image.open("classes/utils/icons/edit-pen-icon-18.jpg")
        self.icon_modify = self.icon_modify.resize((22, 22))
        self.icon_modify = ImageTk.PhotoImage(self.icon_modify)

        self.icon_save = Image.open("classes/utils/icons/save-image-icon-11.jpg")
        self.icon_save = self.icon_save.resize((22, 22))
        self.icon_save = ImageTk.PhotoImage(self.icon_save)

        self.icon_refresh = Image.open("classes/utils/icons/reset-icon-png-10.jpg")
        self.icon_refresh = self.icon_refresh.resize((22, 22))
        self.icon_refresh = ImageTk.PhotoImage(self.icon_refresh)

        self.scadente_frame = tk.LabelFrame(self.master, text="Scadente")
        self.scadente_frame.pack(padx=5, pady=5)

        self.scadenta_noua_label = tk.Label(self.scadente_frame, text="Adauga scadenta:")
        self.scadenta_noua_label.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.scadenta_noua_button = tk.Button(self.scadente_frame, image=self.icon_new, borderwidth=0, highlightthickness=0, relief="flat", command=self.adauga_scadenta_rem)
        self.scadenta_noua_button.grid(row=0, column=1, sticky=W, padx=10, pady=10)
        ToolTip(self.scadenta_noua_button, text="Adauga scadenta")

        self.refresh_scadente = tk.Button(self.scadente_frame, image=self.icon_refresh, borderwidth=0, highlightthickness=0, relief="flat", command=self.incarca_scadente)
        self.refresh_scadente.grid(row=0, column=2, sticky=W, padx=10, pady=10)
        ToolTip(self.refresh_scadente, text="Refresh")
        
        lista_scadente = self.incarca_scadente()

        if lista_scadente:

            for i, scadenta in enumerate(lista_scadente):
                # Debug code - verificam daca lista e ok
                print(i, scadenta)
                i += 1
                b = 0
                if (date.today() + timedelta(days=15)) >= scadenta[1] - timedelta(days=15):
                    self.label_name = tk.Label(self.scadente_frame, text=f"{scadenta[0]}:  {scadenta[1]} ", fg="red")
                    self.label_name.grid(row=i, column=b, sticky="w", padx=10, pady=5)
                    self.edit_button = tk.Button(self.scadente_frame, image=self.icon_modify, borderwidth=0, highlightthickness=0, relief="flat", command=lambda label=scadenta[0] : self.modifica_scadenta(label))
                    self.edit_button.grid(row=i, column=b+1, sticky="w", padx=10, pady=5)
                    ToolTip(self.edit_button, text="Modifica scadenta")

                    self.delete_button = tk.Button(self.scadente_frame, image=self.icon_delete, borderwidth=0, highlightthickness=0, relief="flat", command=lambda label=scadenta[0] : self.sterge_scadenta(label))
                    self.delete_button.grid(row=i, column=b+2, sticky="w", padx=2, pady=5)
                    ToolTip(self.delete_button, text="Sterge scadenta")
                    
        
                    # tk.Label(self.scadente_frame, text=f"{scadenta[1]}", fg="red").grid(row=i+1, column=b+1, sticky="w", padx=10, pady=5)
                else:
                    self.label_name = tk.Label(self.scadente_frame, text=f"{scadenta[0]}:  {scadenta[1]}")
                    self.label_name.grid(row=i, column=b, sticky="w", padx=10, pady=5)
                    self.edit_button = tk.Button(self.scadente_frame, image=self.icon_modify, borderwidth=0, highlightthickness=0, relief="flat", command=lambda label=scadenta[0] : self.modifica_scadenta(label))
                    self.edit_button.grid(row=i, column=b+1, sticky="w", padx=10, pady=5)
                    ToolTip(self.edit_button, text="Modifica scadenta")


                    self.delete_button = tk.Button(self.scadente_frame, image=self.icon_delete, borderwidth=0, highlightthickness=0, relief="flat", command=lambda label=scadenta[0] : self.sterge_scadenta(label))
                    self.delete_button.grid(row=i, column=b+2, sticky="w", padx=2, pady=5)
                    ToolTip(self.delete_button, text="Sterge scadenta")


    def incarca_scadente(self):
        self.lista_scadente = []
        print("Ok")
        connection._open_connection()
        
        sql = "SELECT scadenta, data_scadenta FROM tabel_scadente WHERE id_tms = %s AND nume = %s AND tip = %s"
        values = (self.id_tms, self.nume, self.tip)
        cursor.execute(sql, values)

        self.scadente = cursor.fetchall()

        # Debug - verificam daca lista e ok
        # print(self.scadente)

        if self.scadente:
            for scadenta in self.scadente:
                self.lista_scadente.append(scadenta)
            return self.lista_scadente

        else:
            self.lipsa_scadenta_label = tk.Label(self.scadente_frame, text="Nu exista scadente")
            self.lipsa_scadenta_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)


    def modifica_scadenta_db(self, label):

        try:
            connection._open_connection()
            sql = "UPDATE tabel_scadente SET data_scadenta = %s WHERE id_tms = %s AND nume = %s AND tip = %s AND scadenta = %s"
            values = (self.data_scadenta_entry.get_date(), self.id_tms, self.nume, self.tip, label)
            cursor.execute(sql, values)
            print(values)
            connection.commit()
            messagebox.showinfo(title="Success", message="Scadenta modificata cu succes!")
        
        except:
            messagebox.showerror(title="Error", message="Failed to insert scadenta!")
        finally:
            connection.close()

        self.scadente_frame.pack_forget()
        self.mod_scadenta_window.destroy()

        self.mod_scadenta_frame.pack_forget()

        self.main_window()
        
    
    def modifica_scadenta(self, label):
        print(label)
        print(self.lista_scadente)
        self.mod_scadenta_window = tk.Toplevel(self.master)
        self.mod_scadenta_window.transient(self.master)
        self.mod_scadenta_window.grab_set()
        self.mod_scadenta_window.title("Modifica scadenta")

        self.mod_scadenta_frame = tk.Frame(self.mod_scadenta_window)
        self.mod_scadenta_frame.pack(padx=5, pady=5)

        self.mod_scadenta_label = tk.Label(self.mod_scadenta_frame, text=f"Modifica scadenta: {self.nume}")
        self.mod_scadenta_label.grid(row=0, column=0, sticky="w", padx=10, pady=10, columnspan=3)

        # self.mod_scadenta_entry = DateEntry(self.mod_scadenta_frame, locale="ro_RO", date_pattern="yyyy-mm-dd")
        # self.mod_scadenta_entry.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        self.mod_scadenta_tip_label = tk.Label(self.mod_scadenta_frame, text = f"{label}")
        self.mod_scadenta_tip_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        connection._open_connection()
        sql = "SELECT data_scadenta FROM tabel_scadente WHERE id_tms = %s AND nume = %s AND tip = %s AND scadenta = %s"
        values = (self.id_tms, self.nume, self.tip, label)
        cursor.execute(sql, values)
        self.data_scadenta = cursor.fetchall()
        connection.close()

        self.data_scadenta_entry = DateEntry(self.mod_scadenta_frame, locale="ro_RO", date_pattern="yyyy-mm-dd")
        self.data_scadenta_entry.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        self.data_scadenta_entry.set_date(self.data_scadenta[0][0])


        self.mod_scadenta_save = tk.Button(self.mod_scadenta_frame, text="Salveaza", image=self.icon_save, borderwidth=0, highlightthickness=0, relief="flat", command=lambda label=label: self.modifica_scadenta_db(label))
        self.mod_scadenta_save.grid(row=1, column=2, sticky="w", padx=10, pady=10)
        ToolTip(self.mod_scadenta_save, text="Salveaza")

        self.mod_scadenta_window.wait_window()

    def adauga_scadenta(self):
        print(self.select_scadenta.get())
        print(self.data_scadenta_entry.get_date())

        try:
            connection._open_connection()
            sql = "INSERT INTO tabel_scadente (id_tms, nume, tip, scadenta, data_scadenta) VALUES (%s, %s, %s, %s, %s)"
            values = (self.id_tms, self.nume, self.tip, self.select_scadenta.get(), self.data_scadenta_entry.get_date())
            cursor.execute(sql, values)
            connection.commit()
            messagebox.showinfo(title="Success", message="Scadenta adaugata cu succes!")
            
        
        except:
            messagebox.showerror(title="Error", message="Failed to insert scadenta!")
        finally:
            connection.close()

            self.adauga_scadenta_frame.pack_forget()
            self.adauga_scadenta_window.destroy()
            
            # self.adauga_scadenta_frame.pack_forget()
            self.scadente_frame.pack_forget()

            self.main_window()

    
    def sterge_scadenta(self, label):
        try:
            connection._open_connection()
            sql = "DELETE FROM tabel_scadente WHERE id_tms = %s AND nume = %s AND tip = %s AND scadenta = %s"
            values = (self.id_tms, self.nume, self.tip, label)
            cursor.execute(sql, values)
            connection.commit()
            messagebox.showinfo(title="Success", message="Scadenta stearsa cu succes!")

        except: 
            messagebox.showerror(title="Error", message="Failed to delete scadenta!")

        self.scadente_frame.pack_forget()
        self.main_window()
    

    def adauga_scadenta_rem(self):
        
        def actualizeaza_lista_scadente(e):
            scadente_window = Toplevel(self.master)
            scadente_window.transient(self.master)
            scadente_window.grab_set()
            get_scadente = Scadente_auto(self.master)
            get_scadente.adauga_tip_scadenta(scadente_window)
            scadente_window.wait_window()
            lista_scadente = get_scadente.afisare_scadente()
            self.select_scadenta.configure(values=lista_scadente)

        self.adauga_scadenta_window = tk.Toplevel(self.master)
        self.adauga_scadenta_window.transient(self.master)
        self.adauga_scadenta_window.grab_set()
        self.adauga_scadenta_window.title("Adauga scadenta")

        self.adauga_scadenta_frame = tk.Frame(self.adauga_scadenta_window)
        self.adauga_scadenta_frame.pack()

        self.adauga_scadenta_label = tk.Label(self.adauga_scadenta_frame, text="Tip scadenta:")
        self.adauga_scadenta_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.tip_scadente = Scadente_auto(self.adauga_scadenta_frame)
        self.tip_scadente_list = self.tip_scadente.afisare_scadente()

        self.select_scadenta = ttk.Combobox(self.adauga_scadenta_frame, values = self.tip_scadente_list, width=12)
        self.select_scadenta.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        self.select_scadenta.bind("<Double-1>", actualizeaza_lista_scadente)

        self.data_scadenta_label = tk.Label(self.adauga_scadenta_frame, text="Data scadenta:")
        self.data_scadenta_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.data_scadenta_entry = DateEntry(self.adauga_scadenta_frame, locale="ro_RO", date_pattern='yyyy-MM-dd')
        self.data_scadenta_entry.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        self.adauga_scadenta_button = tk.Button(self.adauga_scadenta_frame, text="Adauga", image=self.icon_save, borderwidth=0, highlightthickness=0, relief="flat", command=self.adauga_scadenta)
        self.adauga_scadenta_button.grid(row=1, column=2, sticky="w", padx=10, pady=10)
        ToolTip(self.adauga_scadenta_button, text="Salveaza")

        self.adauga_scadenta_window.wait_window()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scadente")
    # registru = Scadente(root, 9, "AR11YHA", "SEMIREMORCA")
    # # registru.main_window(root)
    # # root.protocol("WM_DELETE_WINDOW", on_closing)
    # root.mainloop()
    new_scadenta = Scadente_directe(root, 3, "AR03LDF", "SEMIREMORCA", "INVENTAR", "2024-09-11")
    root.mainloop()
