from tkinter import *
from tkinter import ttk, messagebox
from datetime import date
import mysql.connector
import os
from dotenv import load_dotenv
from classes.check_vat import *


root = Tk()
root.title("Adaugare firma")
root.geometry("900x600")

load_dotenv()

salvat = False

# Create connection to database
try:
    tms_db = mysql.connector.connect(
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
my_cursor = tms_db.cursor()

my_cursor.execute("CREATE TABLE IF NOT EXISTS clienti (client_id INT AUTO_INCREMENT PRIMARY KEY, \
                  denumire VARCHAR(255) NOT NULL, \
                  cui_tara VARCHAR(255), \
                  cui_nr INT(20) NOT NULL, \
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
                  fara_tva INT(1), \
                  facturabil INT(1), \
                  is_client INT(1), \
                  is_supplier INT(1), \
                  blocat INT(1), \
                  zile_incasare VARCHAR(15), \
                  perioada_incasare VARCHAR(15), \
                  zile_plata VARCHAR(15), \
                  perioada_plata VARCHAR(15), \
                  banca VARCHAR(255), \
                  iban_ron VARCHAR(255), \
                  iban_eur VARCHAR(255), \
                  swift VARCHAR(255), \
                  pers_contact VARCHAR(255), \
                  telefon VARCHAR(25), \
                  email VARCHAR(255), \
                  web VARCHAR(255), \
                  UNIQUE (denumire, cui_nr, reg_com))")

# my_cursor.execute("SELECT * FROM clienti")
# print(my_cursor.description)

# root.grid_columnconfigure((0,1), weight=1)

# Golire campuri dupa salvarea clientului

# Salvare client din taste
def save_client(e):
    add_client()

# Verificam daca e salvat clientul inainte sa se inchida fereastra
def on_closing():
    if salvat == False:
        if messagebox.askokcancel("Inchidere", "Doriti sa inchideti fereastra?"):
            root.destroy()
    else:
        root.destroy()

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
    inactiv_check.deselect()
    platitor_tva.deselect()
    facturabil.deselect()
    client_check.deselect()
    furnizor_check.deselect()
    blocat_check.deselect()
    nr_zile_incasare_input.delete(0, END)
    tip_incasare.set("data_in_out")
    nr_zile_plata_input.delete(0, END)
    tip_plata.set("data_in_out")
    banca_input.delete(0, END)
    cont_ron_input.delete(0, END)
    cont_eur_input.delete(0, END)
    swift_input.delete(0, END)
    persoana_input.delete(0, END)
    tel_input.delete(0, END)
    email_input.delete(0, END)
    www_input.delete(0, END)

# Anulare introducere client
def anulare_client():
    confirm_cancel = messagebox.askyesno(title="Anulare inregistrare", message="Sigur anulam?")
    if confirm_cancel:
        clear_fields()
    

# Adaugare client in baza de date
def add_client():
    global salvat
    if nume_firma_input.get() and cui_firma_nr.get() and reg_com_input.get():
    
        sql_command = "INSERT INTO clienti (denumire, cui_tara, cui_nr, reg_com, oras, judet, tara, cod_postal, tip_tara, sediu_social, e_factura, tva_incasare, inactiv, fara_tva, facturabil, is_client, is_supplier, blocat, zile_incasare, perioada_incasare, zile_plata, perioada_plata, banca, iban_ron, iban_eur, swift, pers_contact, telefon, email, web) VALUES \
                        (%s, %s, %s, %s, %s, %s, \
                        %s, %s, %s, %s, %s, \
                        %s, %s, %s, %s, %s, \
                        %s, %s, %s, %s, %s, \
                        %s, %s, %s, %s, %s, \
                        %s, %s, %s, %s)"
        values = (nume_firma_input.get(), 
                cui_firma_tara.get(), 
                int(cui_firma_nr.get()), 
                reg_com_input.get(), 
                oras_input.get(), 
                judet_input.get(), 
                tara_input.get(), 
                cod_postal_input.get(), 
                tip_tara_select.get(), 
                sediu_social_input.get(), 
                var_efactura.get(), 
                var_tvaincasare.get(), 
                var_inactiv.get(),
                var_tva.get(),
                var_facturabil.get(),
                var_client.get(),
                var_furnizor.get(),
                var_blocat.get(),
                nr_zile_incasare_input.get(),
                tip_incasare.get(),
                nr_zile_plata_input.get(),
                tip_plata.get(),
                banca_input.get(),
                cont_ron_input.get(),
                cont_eur_input.get(),
                swift_input.get(),
                persoana_input.get(),
                tel_input.get(),
                email_input.get(),
                www_input.get())
        try:
            my_cursor.execute(sql_command, values)
        except mysql.connector.Error as err:
            # print("Something went wrong: {}".format(err))
            if str(err).split(" ")[0] == "1062":
                error = messagebox.showerror(title="Eroare", message="Mai exista un client cu aceste date")
        else:    
            
            # Commit data to DB
            tms_db.commit()
            adaugare_client.configure(state=DISABLED)
            salvat = True
            confirmation = messagebox.showinfo(title="Adaugare client nou", message="Clientul a fost adaugat")
            refresh()

    else:
        error_msg = messagebox.showerror(title="Eroare", message="Va rog completati campurile obligatorii.")

# Actualizare Id
def refresh():
    get_id = "SELECT client_id FROM clienti WHERE LOCATE(%s,denumire)>0"
    search_field = nume_firma_input.get()
    search = (search_field, )
    result = my_cursor.execute(get_id, search)
    result = my_cursor.fetchall()
    print(result[0][0])
    client_id.configure(text=f"Numar TMS: {result[0][0]}")
    print(tip_plata.get())

# Preluare date de la VIES
def vies_check():
    if cui_firma_tara.get() and cui_firma_nr.get():
        cui_vies_country = cui_firma_tara.get()
        cui_vies_number = cui_firma_nr.get()
        rezultat = Vies(cui_vies_country, cui_vies_number)
        print(rezultat.check_vies())
        if not rezultat.check_vies():
            information = messagebox.showinfo(title="Negasit", message="CUI negasit.")
    else:
        information = messagebox.showwarning(title="Eroare", message="Te rog completeaza tara si numar VAT")


# Preluare date de la ANAF
def check_anaf():
    if cui_firma_nr.get():
        cui_anaf_number = cui_firma_nr.get()
        if cui_anaf_number.isdigit():
            rezultat = Anaf(cui_anaf_number)
            data = rezultat.check_anaf()

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

            if data["found"][0]["inregistrare_scop_Tva"]["scpTVA"] == False:
                platitor_tva.select()

            print(var_efactura.get())

        else:
            information = messagebox.showerror(title="Eroare", message="CUI nu a fost gasit")

    else:
        information = messagebox.showwarning(title="Eroare", message="Campul CUI nu poate fi gol!")

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

cui_label = Frame(detail_frame)
cui_label.grid(row=1, column=1, sticky="w", columnspan=3)

cui_firma_tara = Entry(cui_label, width=5)
cui_firma_tara.grid(row=0, column=0, sticky="w", pady=5)

cui_firma_nr = Entry(cui_label, justify=LEFT)
cui_firma_nr.grid(row=0, column=1, sticky="w", pady=5)

get_mfinante = Button(cui_label, text="Preluare ANAF", command=check_anaf)
get_mfinante.grid(row=0, column=2, pady=5, sticky="w", padx=5)

get_vies = Button(cui_label, text="Preluare VIES", command=vies_check)
get_vies.grid(row=0, column=3, pady=5, sticky="w", padx=5)

reg_com_label = Label(detail_frame, text="Reg. Com.: ")
reg_com_label.grid(row=2, column=0, pady=5)

reg_com_input = Entry(detail_frame)
reg_com_input.grid(row=2, column=1, pady=5, sticky="w")

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

frame2 = LabelFrame(root, text="Informatii", padx=5, pady=5)
frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

# Creare variabile pentru check boxes
var_efactura = StringVar()
var_tvaincasare = StringVar()
var_inactiv = StringVar()
var_client = StringVar()
var_furnizor = StringVar()
var_blocat = StringVar()
var_tva = StringVar()
var_facturabil = StringVar()

# Variabile de bifat / debifat
efactura_check = Checkbutton(frame2, text="E-Factura", variable=var_efactura, onvalue=True, offvalue=False)
efactura_check.deselect()
efactura_check.grid(row=0, column=0, sticky="w")

tvaincasare_check = Checkbutton(frame2, text="TVA la incasare", variable=var_tvaincasare, onvalue=True, offvalue=False)
tvaincasare_check.deselect()
tvaincasare_check.grid(row=1, column=0, sticky="w")

inactiv_check = Checkbutton(frame2, text="Inactiv", variable=var_inactiv, onvalue=True, offvalue=False)
inactiv_check.deselect()
inactiv_check.grid(row=2, column=0, sticky="w")

platitor_tva = Checkbutton(frame2, text="Neplatitor TVA", variable=var_tva, onvalue=True, offvalue=False)
platitor_tva.deselect()
platitor_tva.grid(row=3, column=0, sticky="w")

facturabil = Checkbutton(frame2, text="Facturabil", variable=var_facturabil, onvalue=True, offvalue=False)
facturabil.deselect()
facturabil.grid(row=4, column=0, sticky="w")

client_check = Checkbutton(frame2, text="Client", variable=var_client, onvalue=True, offvalue=False)
client_check.deselect()
client_check.grid(row=5, column=0, sticky="w")

furnizor_check = Checkbutton(frame2, text="Furnizor", variable=var_furnizor, onvalue=True, offvalue=False)
furnizor_check.deselect()
furnizor_check.grid(row=6, column=0, sticky="w")

blocat_check = Checkbutton(frame2, text="Blocat", variable=var_blocat, onvalue=True, offvalue=False)
blocat_check.deselect()
blocat_check.grid(row=7, column=0, sticky="w")

client_id = Label(frame2, text="Numar TMS:")
client_id.grid(row=8, column=0, sticky="w")

# Detaliile bancare
frame_banca = LabelFrame(root, text="Detalii bancare", padx=10, pady=10)
frame_banca.grid(row=1, column=0, pady=10, padx=10, sticky="nwe")

banca_label = Label(frame_banca, text="Banca: ")
banca_label.grid(row=0, column=0, sticky="w")

banca_input = Entry(frame_banca, width=50)
banca_input.grid(row=0, column=1, sticky="w")

cont_ron_label = Label(frame_banca, text="Cont RON: ")
cont_ron_label.grid(row=1, column=0, sticky="w", pady=5)

cont_ron_input = Entry(frame_banca, width=50)
cont_ron_input.grid(row=1, column=1, sticky="w", pady=5)

cont_eur_label = Label(frame_banca, text="Cont EUR: ")
cont_eur_label.grid(row=2, column=0, sticky="w", pady=5)

cont_eur_input = Entry(frame_banca, width=50)
cont_eur_input.grid(row=2, column=1, sticky="w", pady=5)

swift_label = Label(frame_banca, text="SWIFT: ")
swift_label.grid(row=3, column=0, sticky="w", pady=5)

swift_input = Entry(frame_banca, width=50)
swift_input.grid(row=3, column=1, pady=5, sticky="w")


# Conditii incasare / plata
frame_incasare_plata = LabelFrame(root, text="Conditii incasare/plata", padx=5, pady=5)
frame_incasare_plata.grid(row=0, column=2, sticky="nws", padx=10, pady=10)

frame_incasare = LabelFrame(frame_incasare_plata, text="Incasare", padx=5, pady=5)
frame_incasare.grid(row=0, column=0, sticky="nw")

nr_zile_incasare = Label(frame_incasare, text="Nr. Zile: ")
nr_zile_incasare.grid(row=0, column=0, sticky="w")

nr_zile_incasare_input = Entry(frame_incasare, width=10)
nr_zile_incasare_input.grid(row=0, column=1, sticky="w")

# Radio button pt conditii incasare:

tip_incasare = StringVar()
tip_incasare.set("data_in_out")

Radiobutton(frame_incasare, text="De la data facturii", variable=tip_incasare, value="data_fact").grid(row=1, column=0, sticky="w", columnspan=2)
Radiobutton(frame_incasare, text="De la data primirii/iesirii facturii", variable=tip_incasare, value="data_in_out").grid(row=2, column=0, sticky="w", columnspan=2)

frame_plata = LabelFrame(frame_incasare_plata, text="Plata", padx=5, pady=5)
frame_plata.grid(row=1, column=0, sticky="nw")

nr_zile_plata = Label(frame_plata, text="Nr. Zile: ")
nr_zile_plata.grid(row=0, column=0, sticky="w")

nr_zile_plata_input = Entry(frame_plata, width=10)
nr_zile_plata_input.grid(row=0, column=1, sticky="w")

# Radio button pt conditii plata:

tip_plata = StringVar()
tip_plata.set("data_in_out")

Radiobutton(frame_plata, text="De la data facturii", variable=tip_plata, value="data_fact").grid(row=1, column=0, sticky="w", columnspan=2)
Radiobutton(frame_plata, text="De la data primirii/iesirii facturii", variable=tip_plata, value="data_in_out").grid(row=2, column=0, sticky="w", columnspan=2)

# Butoanele de salvare, anulare, verificare
frame_butoane = LabelFrame(root, text = "Adaugare / Anulare", padx=10, pady=10)
frame_butoane.grid(row=2, column=0, pady=10, padx=10, sticky="nw")

adaugare_client = Button(frame_butoane, text="Adaugare", command = add_client)
adaugare_client.grid(row=0, column=0, sticky="we")

anulare_adaugare = Button(frame_butoane, text="Anulare", command=anulare_client)
anulare_adaugare.grid(row=0, column=1, padx=5, sticky="we")

afisare_tot = Button(frame_butoane, text="Afisare", command=refresh)
afisare_tot.grid(row=0, column=2, padx=5, sticky="we")


# Frame cu datele de contact
frame_contact = LabelFrame(root, text="Date contact", padx=10, pady=10)
frame_contact.grid(row=1, column=1, pady=10, padx=10, sticky="nwe", columnspan=2)

persoana_label = Label(frame_contact, text="Persoana contact: ")
persoana_label.grid(row=0, column=0, sticky="w")

persoana_input = Entry(frame_contact, width=40)
persoana_input.grid(row=0, column=1, sticky="w")

tel_label = Label(frame_contact, text="Telefon: ")
tel_label.grid(row=1, column=0, sticky="w", pady=5)

tel_input = Entry(frame_contact, width=40)
tel_input.grid(row=1, column=1, sticky="w", pady=5)

email_label = Label(frame_contact, text="Email: ")
email_label.grid(row=2, column=0, sticky="w", pady=5)

email_input = Entry(frame_contact, width=40)
email_input.grid(row=2, column=1, sticky="w", pady=5)

www_label = Label(frame_contact, text="Web: ")
www_label.grid(row=3, column=0, sticky="w", pady=5)

www_input = Entry(frame_contact, width=40)
www_input.grid(row=3, column=1, sticky="w", pady=5)

root.bind('<Control-s>', save_client)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
