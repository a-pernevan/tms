from tkinter import *
from tkinter import ttk, messagebox
import requests
from datetime import date
import json
import mysql.connector
import os
from dotenv import load_dotenv


root = Tk()
root.title("Adaugare firma")
root.geometry("800x600")

load_dotenv()

# Create connection to database
tms_db = mysql.connector.connect(
    host = os.getenv("HOST"),
    user = os.getenv("USER"),
    passwd = os.getenv("PASS"),
    database = os.getenv("DB"),
    auth_plugin='mysql_native_password'
)

my_cursor = tms_db.cursor()

my_cursor.execute("CREATE TABLE IF NOT EXISTS clienti (denumire VARCHAR(255), \
                  cui_tara VARCHAR(255), \
                  cui_nr INT(20), \
                  reg_com VARCHAR(255), \
                  oras VARCHAR(255), \
                  judet VARCHAR(255), \
                  tara VARCHAR(255), \
                  cod_postal VARCHAR(255), \
                  tip_tara VARCHAR(10), \
                  sediu_social VARCHAR(255),\
                  e_factura INT(1), \
                  tva_incasare INT(1), \
                  inactiv INT(1), \
                  client_id INT AUTO_INCREMENT PRIMARY KEY)")

# my_cursor.execute("SELECT * FROM clienti")
# print(my_cursor.description)

# root.grid_columnconfigure((0,1), weight=1)

# Golire campuri dupa salvarea clientului

def clear_fields():
    nume_firma_input.delete(0, END)
    cui_firma_tara.delete(0, END)
    cui_firma_nr.delete(0, END)
    reg_com_input.delete(0, END)
    oras_input.delete(0, END)
    judet_input.delete(0, END)
    tara_input.delete(0, END)
    cod_postal_input.delete(0, END)
    tip_tara_select.current(0)
    sediu_social_input.delete(0, END)
    efactura_check.deselect()
    tvaincasare_check.deselect()

# Anulare introducere client
def anulare_client():
    confirm_cancel = messagebox.askyesno(title="Anulare inregistrare", message="Sigur anulam?")
    if confirm_cancel:
        clear_fields()
    

# Adaugare client in baza de date
def add_client():
    sql_command = "INSERT INTO clienti (denumire, cui_tara, cui_nr, reg_com, oras, judet, tara, cod_postal, tip_tara, sediu_social, e_factura, tva_incasare, inactiv) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (nume_firma_input.get(), cui_firma_tara.get(), cui_firma_nr.get(), reg_com_input.get(), oras_input.get(), judet_input.get(), tara_input.get(), cod_postal_input.get(), tip_tara_select.get(), sediu_social_input.get(), var_efactura.get(), var_tvaincasare.get(), var_inactiv.get())
    my_cursor.execute(sql_command, values)

    # Commit data to DB
    tms_db.commit()

    confirmation = messagebox.showinfo(title="Adaugare client nou", message="Clientul a fost adaugat")
    refresh()


# Printare date
def refresh():
    get_id = "SELECT client_id FROM clienti WHERE LOCATE(%s,denumire)>0"
    search_field = nume_firma_input.get()
    search = (search_field, )
    result = my_cursor.execute(get_id, search)
    result = my_cursor.fetchall()
    print(result[0][0])
    client_id.configure(text=f"Numar TMS: {result[0][0]}")

# Preluare date de la ANAF
def check_anaf():
    query_params = [{
    "cui": cui_firma_nr.get(),
    "data": date.today().strftime("%Y-%m-%d")
    }]
    headers = {"Content-Type": "application/json"}
    api_addr = "https://webservicesp.anaf.ro/PlatitorTvaRest/api/v8/ws/tva"
    response = requests.post(api_addr, data=json.dumps(query_params), headers=headers)
    data = response.json()

    if data["found"]:
        nume_firma_input.insert(0, data["found"][0]["date_generale"]["denumire"])
        reg_com_input.insert(0, data["found"][0]["date_generale"]["nrRegCom"])
        oras_input.insert(0, data["found"][0]["adresa_sediu_social"]["sdenumire_Localitate"])
        judet_input.insert(0, data["found"][0]["adresa_sediu_social"]["sdenumire_Judet"])
        tara_input.insert(0, "Romania")
        cod_postal_input.insert(0, data["found"][0]["adresa_sediu_social"]["scod_Postal"])
        sediu_social_input.insert(0, data["found"][0]["date_generale"]["adresa"])
        if data["found"][0]["date_generale"]["statusRO_e_Factura"]:
            efactura_check.select()
        
        if data["found"][0]["inregistrare_RTVAI"]["statusTvaIncasare"]:
            tvaincasare_check.select()

        if data["found"][0]["stare_inactiv"]["statusInactivi"]:
            inactiv_check.select()

        print(var_efactura.get())

tara_values = [
    "",
    "UE",
    "NON-UE",
    "Romania"
]

# Creare interfata TKinter
detail_frame = LabelFrame(root, text="Detalii firma", padx=10, pady=10)
detail_frame.grid(row=0, column=0, padx=10, pady=10)

nume_firma_label = Label(detail_frame, text="Nume:* ")
nume_firma_label.grid(row=0, column=0, sticky="w")

nume_firma_input = Entry(detail_frame, width=50)
nume_firma_input.grid(row=0, column=1, columnspan=3, sticky="w")

cui_firma_label = Label(detail_frame, text="CUI:* ", anchor="e", justify=LEFT)
cui_firma_label.grid(row=1, column=0, sticky="w", pady=5)

cui_firma_tara = Entry(detail_frame, width=5)
cui_firma_tara.grid(row=1, column=1, sticky="w", pady=5)

cui_firma_nr = Entry(detail_frame, justify=LEFT)
cui_firma_nr.grid(row=1, column=2, sticky="w", pady=5)

get_mfinante = Button(detail_frame, text="Preluare ANAF", command=check_anaf)
get_mfinante.grid(row=1, column=3, pady=5, sticky="w", padx=5)

reg_com_label = Label(detail_frame, text="Reg. Com.: ")
reg_com_label.grid(row=2, column=0, pady=5)

reg_com_input = Entry(detail_frame)
reg_com_input.grid(row=2, column=1, pady=5, sticky="w", columnspan=2)

oras_label = Label(detail_frame, text="Oras: ")
oras_label.grid(row=3, column=0, sticky="w", pady=5)

oras_input = Entry(detail_frame)
oras_input.grid(row=3, column=1, sticky="w", pady=5)

judet_label = Label(detail_frame, text="Judet: ")
judet_label.grid(row=3, column=2, sticky="e", pady=5)

judet_input = Entry(detail_frame)
judet_input.grid(row=3, column=3, sticky="w", pady=5)

tara_label = Label(detail_frame, text="Tara: ")
tara_label.grid(row=4, column=0, sticky="w", pady=5)

tara_input = Entry(detail_frame)
tara_input.grid(row=4, column=1, sticky="w", columnspan=2, pady=5)

cod_postal_label = Label(detail_frame, text="Cod Postal: ")
cod_postal_label.grid(row=4, column=2, sticky="e", pady=5)

cod_postal_input = Entry(detail_frame)
cod_postal_input.grid(row=4, column=3, sticky="w", pady=5)

tip_tara_label = Label(detail_frame, text="Tip Tara: ")
tip_tara_label.grid(row=5, column=0, sticky="w", pady=5)

tip_tara_select = ttk.Combobox(detail_frame, value=tara_values)
tip_tara_select.current(0)
tip_tara_select.grid(row=5, column=1, sticky="w", pady=5, columnspan=2)

sediu_social_label = Label(detail_frame, text="Sediu Social: ")
sediu_social_label.grid(row=6, column=0, sticky="w", pady=5)

sediu_social_input = Entry(detail_frame, width=50)
sediu_social_input.grid(row=6, column=1, columnspan=3, sticky="w", pady=5)

frame2 = LabelFrame(root, text="Informatii", padx=10, pady=10)
frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nw", rowspan=6)

var_efactura = StringVar()
var_tvaincasare = StringVar()
var_inactiv = StringVar()

efactura_check = Checkbutton(frame2, text="E-Factura", variable=var_efactura, onvalue=True, offvalue=False)
efactura_check.deselect()
efactura_check.grid(row=0, column=0, sticky="w")

tvaincasare_check = Checkbutton(frame2, text="TVA la incasare", variable=var_tvaincasare, onvalue=True, offvalue=False)
tvaincasare_check.deselect()
tvaincasare_check.grid(row=1, column=0, sticky="w")

inactiv_check = Checkbutton(frame2, text="Inactiv", variable=var_inactiv, onvalue=True, offvalue=False)
inactiv_check.deselect()
inactiv_check.grid(row=2, column=0, sticky="w")

client_id = Label(frame2, text="Numar TMS:")
client_id.grid(row=3, column=0, sticky="w")

frame3 = LabelFrame(root, text = "Adaugare / Anulare", padx=10, pady=10)
frame3.grid(row=1, column=0, pady=10)

adaugare_client = Button(frame3, text="Adaugare", command = add_client)
adaugare_client.grid(row=0, column=0)

anulare_adaugare = Button(frame3, text="Anulare", command=anulare_client)
anulare_adaugare.grid(row=0, column=1, padx=5)

afisare_tot = Button(frame3, text="Afisare", command=refresh)
afisare_tot.grid(row=0, column=2, padx=5)

root.mainloop()
