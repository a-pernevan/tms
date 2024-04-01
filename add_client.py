from tkinter import *
from tkinter import ttk
import requests
from datetime import date
import json


root = Tk()
root.title("Adaugare firma")
root.geometry("800x600")

# root.grid_columnconfigure((0,1), weight=1)

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

root.mainloop()
