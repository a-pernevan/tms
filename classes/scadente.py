from multiprocessing import Value
import tkinter as tk
from tkinter import Label, LabelFrame, Toplevel, ttk
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

class Scadente:
    def __init__(self, master, id_tms, nume, tip):
        self.master = master
        self.id_tms = id_tms
        self.nume = nume
        self.tip = tip
        self.lista_scadente = []

        connection._open_connection()

    def main_window(self, master):
        self.icon_new = Image.open("classes/utils/icons/add-text-icon-15.jpg")
        self.icon_new = self.icon_new.resize((22, 22))
        self.icon_new = ImageTk.PhotoImage(self.icon_new)

        self.icon_delete = Image.open("classes/utils/icons/icon-delete-19.jpg")
        self.icon_delete = self.icon_delete.resize((22, 22))
        self.icon_delete = ImageTk.PhotoImage(self.icon_delete)

        self.icon_modify = Image.open("classes/utils/icons/edit-pen-icon-18.jpg")
        self.icon_modify = self.icon_modify.resize((22, 22))
        self.icon_modify = ImageTk.PhotoImage(self.icon_modify)

        self.scadente_frame = tk.LabelFrame(master, text="Scadente")
        self.scadente_frame.pack(padx=5, pady=5)

        self.scadenta_noua_label = tk.Label(self.scadente_frame, text="Adauga scadenta:")
        self.scadenta_noua_label.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.scadenta_noua_button = tk.Button(self.scadente_frame, image=self.icon_new, borderwidth=0, highlightthickness=0, relief="flat", command=self.incarca_scadente)
        self.scadenta_noua_button.grid(row=0, column=1, sticky=W, padx=10, pady=10)
        ToolTip(self.scadenta_noua_button, text="Adauga scadenta")
        
        self.incarca_scadente()
        for i, scadenta in enumerate(self.lista_scadente):
            # Debug code - verificam daca lista e ok
            # print(i, scandenta)
            i += 1
            b = 0
            if (date.today() + timedelta(days=15)) >= scadenta[1] - timedelta(days=15):
                self.label_name = f"{scadenta[0]}"
                self.label_name = tk.Label(self.scadente_frame, text=f"{scadenta[0]}:  {scadenta[1]} ", fg="red")
                self.label_name.grid(row=i, column=b, sticky="w", padx=10, pady=5)
                self.edit_button = tk.Button(self.scadente_frame, image=self.icon_modify, borderwidth=0, highlightthickness=0, relief="flat", command=lambda label=scadenta[0] : self.modifica_scadenta(label))
                self.edit_button.grid(row=i, column=b+1, sticky="w", padx=10, pady=5)
                ToolTip(self.edit_button, text="Modifica scadenta")
                
    
                # tk.Label(self.scadente_frame, text=f"{scadenta[1]}", fg="red").grid(row=i+1, column=b+1, sticky="w", padx=10, pady=5)
            else:
                self.label_name = f"{scadenta[0]}"
                self.label_name = tk.Label(self.scadente_frame, text=f"{scadenta[0]}:  {scadenta[1]}")
                self.label_name.grid(row=i, column=b, sticky="w", padx=10, pady=5)
                self.edit_button = tk.Button(self.scadente_frame, image=self.icon_modify, borderwidth=0, highlightthickness=0, relief="flat", command=lambda label=scadenta[0] : self.modifica_scadenta(label))
                self.edit_button.grid(row=i, column=b+1, sticky="w", padx=10, pady=5)
                ToolTip(self.edit_button, text="Modifica scadenta")
                
                

        

    def incarca_scadente(self):
        
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
    
    def modifica_scadenta(self, label):
        print(label)
        print(self.label_name)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scadente")
    registru = Scadente(root, 35, "AR15UUT", "SEMIREMORCA")
    registru.main_window(root)
    # root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()