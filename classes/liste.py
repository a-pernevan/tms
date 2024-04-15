from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class Functii:
    def __init__(self, master):
        self.lista_functii = []
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
        self.my_cursor.execute("CREATE TABLE IF NOT EXISTS functii (functie_id INT AUTO_INCREMENT PRIMARY KEY, denumire VARCHAR(120) NOT NULL, grupa VARCHAR(120), UNIQUE(denumire))")
        self.my_cursor.execute("SELECT * FROM functii")
        self.result = self.my_cursor.fetchall()
        if self.result:
            for self.functie in self.result:
                self.lista_functii.append(self.functie[1])
            self.afisare_functii()
        else:
            messagebox.showerror(title="Error", message="No data found")
            self.adauga_functie(master)

        

    def adauga_functie(self, master):
        self.main_window = master
        self.main_window.title("Administrare Functii")
        
        self.main_frame = LabelFrame(self.main_window, text="Adaugare Functie")
        self.main_frame.pack()
        self.functie_label = Label(self.main_frame, text="Functie: ")
        self.functie_label.grid(row=0, column=0, sticky="nw")

        self.functie_entry = Entry(self.main_frame)
        self.functie_entry.grid(row=0, column=1, sticky="nw")

        self.grup_label = Label(self.main_frame, text="Grup: ")
        self.grup_label.grid(row=1, column=0, sticky="nw")

        self.grup_entry = Entry(self.main_frame)
        self.grup_entry.grid(row=1, column=1, sticky="nw")

        self.functie_button = Button(self.main_frame, text="Adaugare", command=self.adauga)
        self.functie_button.grid(row=2, column=1, sticky="nw")

    def adauga(self):
        self.my_cursor.execute("INSERT INTO functii (denumire, grupa) VALUES (%s, %s)", (self.functie_entry.get(), self.grup_entry.get()))
        self.tms_db.commit()
        messagebox.showinfo(title="Success", message="Functie adaugata")
        self.actualizare_functii()
        self.main_window.destroy()



    def afisare_functii(self):
        return self.lista_functii

    def actualizare_functii(self):
        self.my_cursor.execute("SELECT * FROM functii")
        self.result = self.my_cursor.fetchall()
        for self.functie in self.result:
                self.lista_functii.append(self.functie[1])
        self.afisare_functii()

# class add_functie(Functii):
#     def __init__(self):
#         super().__init__
#         Functii.adauga_functie(self)


if __name__ == "__main__":
    root = Tk()
    root.title("Administrare Functii")
    root.geometry("500x500")

    hello = Functii(root)

    root.mainloop()