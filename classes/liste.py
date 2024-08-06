from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import os
from dotenv import load_dotenv

try:
    from database.datab import connection, cursor
except:
    mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server, program will exit")
    quit()

load_dotenv()

# Se definesc functiile ocupate de angajati in cadrul companiei
# Se definesc si grupurile din care fac parte. 
class Functii:
    def __init__(self, master):
        super().__init__()
        self.lista_functii = []
        # Conexiunea la baza de date
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
            self.mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server")
            quit()
        self.my_cursor = self.tms_db.cursor()
        # Cream tabelul pentru functiile angajatilor
        self.my_cursor.execute("CREATE TABLE IF NOT EXISTS functii (functie_id INT AUTO_INCREMENT PRIMARY KEY, denumire VARCHAR(120) NOT NULL, grupa VARCHAR(120), UNIQUE(denumire))")
        self.my_cursor.execute("SELECT * FROM functii")
        self.result = self.my_cursor.fetchall()
        # Daca exista inregistrari le adaugam in lista
        if self.result:
            for self.functie in self.result:
                self.lista_functii.append(self.functie[1])
            self.afisare_functii()
        else:
            messagebox.showerror(title="Error", message="No data found")
        
    # Se adauga o funcite noua
    def adauga_functie(self, master):
        self.main_window = master
        self.main_window.title("Administrare Functii")
        
        self.main_frame = LabelFrame(self.main_window, text="Adaugare Functie")
        self.main_frame.pack(padx=10, pady=10)
        self.functie_label = Label(self.main_frame, text="Functie: ")
        self.functie_label.grid(row=0, column=0, sticky="nw")

        self.functie_entry = Entry(self.main_frame)
        self.functie_entry.grid(row=0, column=1, sticky="nw", pady=10, padx=5)

        self.grup_label = Label(self.main_frame, text="Grup: ")
        self.grup_label.grid(row=1, column=0, sticky="nw")

        self.grup_entry = Entry(self.main_frame)
        self.grup_entry.grid(row=1, column=1, sticky="nw", pady=10, padx=5)

        self.functie_button = Button(self.main_frame, text="Adaugare", command=self.adauga)
        self.functie_button.grid(row=2, column=1, sticky="nw")

    #Adaugare functie noua in baza de date
    def adauga(self):
        try:
            self.my_cursor.execute("INSERT INTO functii (denumire, grupa) VALUES (%s, %s)", (self.functie_entry.get(), self.grup_entry.get()))
        except mysql.connector.Error as err:
            
            if str(err).split(" ")[0] == "1062":
                messagebox.showerror(title="Eroare", message="Mai exista aceasta functie")
        else:
            self.tms_db.commit()
            messagebox.showinfo(title="Success", message="Functie adaugata")
        self.actualizare_functii()
        
        self.main_window.destroy()
    # Se returneaza lista de functii
    def afisare_functii(self):
        return self.lista_functii

    # Actualizare lista dupa ce se adauga una noua
    def actualizare_functii(self):
        self.my_cursor.execute("SELECT * FROM functii")
        self.result = self.my_cursor.fetchall()
        self.lista_functii = []
        for self.functie in self.result:
                self.lista_functii.append(self.functie[1])
        self.afisare_functii()


class Filiala():
    def __init__(self, master):
        super().__init__()
        self.lista_filiale = []
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
            messagebox.showerror(title="Connection error", message="Could not connect to DB Server")
            quit()

        self.my_cursor = self.tms_db.cursor()
        self.my_cursor.execute("CREATE TABLE IF NOT EXISTS filiale (filiala_id INT AUTO_INCREMENT PRIMARY KEY, denumire VARCHAR(120) NOT NULL, UNIQUE(denumire))")
        self.my_cursor.execute("SELECT * FROM filiale")
        self.result = self.my_cursor.fetchall()
        if self.result:
            for self.filiala in self.result:
                self.lista_filiale.append(self.filiala[1])
            self.afisare_filiale() # De creat
        else:
            messagebox.showerror(title="Error", message="No data found")

    def adauga_filiala(self, master):
        self.main_window = master
        self.main_window.title("Administrare Filiale")
        
        self.main_frame = LabelFrame(self.main_window, text="Adaugare Filiala")
        self.main_frame.pack(padx=10, pady=10)
        self.filiala_label = Label(self.main_frame, text="Filiala: ")
        self.filiala_label.grid(row=0, column=0, sticky="nw")

        self.filiala_entry = Entry(self.main_frame)
        self.filiala_entry.grid(row=0, column=1, sticky="nw", pady=10, padx=5)

        self.filiala_button = Button(self.main_frame, text="Adaugare", command=self.adauga)
        self.filiala_button.grid(row=2, column=1, sticky="nw")

        
    def afisare_filiale(self):
        return self.lista_filiale
    
    def adauga(self):
        try:
            self.my_cursor.execute("INSERT INTO filiale (denumire) VALUES (%s)", (self.filiala_entry.get(),))
        except mysql.connector.Error as err:
            
            if str(err).split(" ")[0] == "1062":
                messagebox.showerror(title="Eroare", message="Mai exista aceasta filiala")
        else:
            self.tms_db.commit()
            messagebox.showinfo(title="Success", message="Filiala adaugata")
        self.actualizare_filiale()
        
        self.main_window.destroy()

    def actualizare_filiale(self):
        self.my_cursor.execute("SELECT * FROM filiale")
        self.result = self.my_cursor.fetchall()
        self.lista_filiale = []
        for self.filiala in self.result:
                self.lista_filiale.append(self.filiala[1])
        self.afisare_filiale()


class Remorci():
    def __init__(self, master):
        super().__init__()
        self.main_window = master

    def afisare_remorci(self):
        lista_remorci = []
        try:
            connection._open_connection()
            cursor.execute("SELECT plate_no FROM tauros_truck WHERE categorie='SEMIREMORCA'")
                           
        except:
            messagebox.messagebox.showerror(title="Connection error", message="Could not connect to DB Server")

        self.nr_remorca = cursor.fetchall()
        connection.close()
        for remorca in self.nr_remorca:
            lista_remorci.append(remorca[0])
        return lista_remorci
    
class Auto():
    pass

class Clienti():
    def __init__(self, master):
        super().__init__()
        self.main_window = master

    def afisare_clienti(self):
        lista_clienti = []
        try:
            connection._open_connection()
            cursor.execute("SELECT client_id, denumire, cui_tara, cui_nr FROM clienti")
                           
        except:
            messagebox.messagebox.showerror(title="Connection error", message="Could not connect to DB Server")

        self.clienti = cursor.fetchall()
        connection.close()
        for client in self.clienti:
            lista_clienti.append(client)

        return lista_clienti  
        