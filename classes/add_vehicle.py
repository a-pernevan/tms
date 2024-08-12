from tkinter import *
from tkinter import ttk, messagebox
# from tkinter.tix import ComboBox
from liste import Remorci
from datetime import datetime, timedelta, date
from upload_download_docs import Documente
from scadente import Scadente
try:
    from database.datab import connection, cursor
except:
    mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server, program will exit")
    quit()

class Vehicule:
    # modificarea vehiculelor
    def __init__(self, root):
        remorci = Remorci.afisare_remorci(root)
        self.root = root
        self.lista_remorci = []
        
        self.main_frame = ttk.Notebook(self.root, width=1300, height=600)
        # self.main_frame = ttk.Notebook(self.root)
        self.main_frame.pack(fill=BOTH, expand=1)

        self.frame_remorci()

    def frame_remorci(self):

        self.remorca_frame = Frame(self.main_frame)
        self.remorca_frame.pack(fill=BOTH, expand=1, anchor=W)

        self.main_frame.add(self.remorca_frame, text="Gestionare remorci")

        self.vehicule_frame = LabelFrame(self.remorca_frame, text="Lista Semiremorci")
        self.vehicule_frame.pack()

        self.frame_cautare = Frame(self.vehicule_frame)
        self.frame_cautare.pack(pady=10, anchor=W)
        
        self.cautare_remorci_label = Label(self.frame_cautare, text="Cautare:")
        self.cautare_remorci_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        # self.remorca_plate = ttk.Combobox(self.vehicule_frame, values=remorci)
        self.remorca_plate = Entry(self.frame_cautare)
        self.remorca_plate.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        self.remorca_table_frame = Frame(self.vehicule_frame)
        self.remorca_table_frame.pack()

        remorca_scrool = Scrollbar(self.remorca_table_frame)
        remorca_scrool.pack(side=RIGHT, fill=Y)

        self.remorca_table = ttk.Treeview(self.remorca_table_frame, columns=("Numar", "Marca", "Serie sasiu", "An fabricatie"))

        remorca_scrool.config(command=self.remorca_table.yview)
        self.remorca_table.config(yscrollcommand=remorca_scrool.set)

        self.remorca_table.heading('#0', text="ID", anchor=CENTER)
        self.remorca_table.heading('Numar', text="Numar", anchor=CENTER)
        self.remorca_table.heading('Marca', text="Marca", anchor=CENTER)
        self.remorca_table.heading('Serie sasiu', text="Serie sasiu", anchor=CENTER)
        self.remorca_table.heading('An fabricatie', text="An fabricatie", anchor=CENTER)

        self.remorca_table.pack(padx=5, pady=5)

        self.incarca_remorci()
        # remorci_list= self.incarca_remorci()
        # for remorca in remorci_list:
        #     print(remorca)

        self.remorca_plate.bind("<KeyRelease>", lambda event: self.cautare_remorci())
        self.remorca_table.bind("<Double-1>", self.incarca_detalii)
        self.remorca_table.bind("<Return>", self.incarca_detalii)

        self.frame_detalii = Frame(self.remorca_frame)
        self.frame_detalii.pack(padx=10, pady=5, anchor=W)

        # self.detalii_remorca()

    def detalii_remorca(self, date_rem, id):

        self.frame_detalii.pack(padx=10, pady=10, anchor=W)

        self.frame_detalii_generale = LabelFrame(self.frame_detalii, text="Detalii Generale")
        self.frame_detalii_generale.grid(row=0, column=0, padx=10, pady=10)

        self.nr_auto_label = Label(self.frame_detalii_generale, text="Numar inmatriculare:")
        self.nr_auto_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.nr_auto = Label(self.frame_detalii_generale, text=date_rem[0])
        self.nr_auto.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        self.marca_label = Label(self.frame_detalii_generale, text="Marca:")
        self.marca_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.marca = Label(self.frame_detalii_generale, text=date_rem[1])
        self.marca.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        self.serie_sasiu_label = Label(self.frame_detalii_generale, text="Serie sasiu:")
        self.serie_sasiu_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.serie_sasiu = Label(self.frame_detalii_generale, text=date_rem[2])
        self.serie_sasiu.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        self.an_fabricatie_label = Label(self.frame_detalii_generale, text="An fabricatie:")
        self.an_fabricatie_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.an_fabricatie = Label(self.frame_detalii_generale, text=date_rem[3])
        self.an_fabricatie.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        self.id_label = Label(self.frame_detalii_generale, text="ID TMS:")
        self.id_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        self.id = Label(self.frame_detalii_generale, text=id)
        self.id.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        
        for remorca in self.lista_remorci:
            if str(id) == str(remorca[0]):
                self.proprietar = Label(self.frame_detalii_generale, text="Proprietar:")
                self.proprietar.grid(row=5, column=0, sticky="w", padx=10, pady=5)

                self.proprietar = Label(self.frame_detalii_generale, text=remorca[5])
                self.proprietar.grid(row=5, column=1, sticky="w", padx=10, pady=5)

        
        connection._open_connection()
        sql = "SELECT * FROM date_tehnice_rem WHERE id_rem=%s"
        value = (id,)
        cursor.execute(sql, value)
        detalii_rem = cursor.fetchall()
        # print(detalii_rem)

        
        self.frame_detalii_tehnice = LabelFrame(self.frame_detalii, text="Detalii Tehnice")
        self.frame_detalii_tehnice.grid(row=0, column=1, padx=10, pady=5)

        if len(detalii_rem) > 0:
            self.frame_detalii_tehnice.grid_forget()
            self.frame_detalii_tehnice.grid(row=0, column=1, padx=10, pady=10)
            # self.frame_detalii_tehnice = LabelFrame(self.frame_detalii, text="Detalii Tehnice")
            # self.frame_detalii_tehnice.grid(row=0, column=1, padx=10, pady=10)

            self.data_inmatriculare_label = Label(self.frame_detalii_tehnice, text="Data primei inmatriculari:")
            self.data_inmatriculare_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

            self.data_inmatriculare = Label(self.frame_detalii_tehnice, text=detalii_rem[0][2])
            self.data_inmatriculare.grid(row=0, column=1, sticky="w", padx=10, pady=5)

            self.serie_civ_label = Label(self.frame_detalii_tehnice, text="Serie CIV:")
            self.serie_civ_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

            self.serie_civ = Label(self.frame_detalii_tehnice, text=detalii_rem[0][3])
            self.serie_civ.grid(row=1, column=1, sticky="w", padx=10, pady=5)

            self.serie_talon_label = Label(self.frame_detalii_tehnice, text="Serie talon:")
            self.serie_talon_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

            self.serie_talon = Label(self.frame_detalii_tehnice, text=detalii_rem[0][4])
            self.serie_talon.grid(row=2, column=1, sticky="w", padx=10, pady=5)

            self.culoare_label = Label(self.frame_detalii_tehnice, text="Culoare:")
            self.culoare_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

            self.culoare = Label(self.frame_detalii_tehnice, text=detalii_rem[0][5])
            self.culoare.grid(row=3, column=1, sticky="w", padx=10, pady=5)

            tip_remorca_label = Label(self.frame_detalii_tehnice, text="Tip remorca:")
            tip_remorca_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

            tip_remorca = Label(self.frame_detalii_tehnice, text=detalii_rem[0][13])
            tip_remorca.grid(row=4, column=1, sticky="w", padx=10, pady=5)

            axe_label = Label(self.frame_detalii_tehnice, text="Numar axe:")
            axe_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)

            axe = Label(self.frame_detalii_tehnice, text=detalii_rem[0][7])
            axe.grid(row=5, column=1, sticky="w", padx=10, pady=5)

            lungime_rem_label = Label(self.frame_detalii_tehnice, text="Lungime:")
            lungime_rem_label.grid(row=0, column=2, sticky="w", padx=10, pady=5)

            lungime_rem = Label(self.frame_detalii_tehnice, text=f"{detalii_rem[0][8]} m")
            lungime_rem.grid(row=0, column=3, sticky="w", padx=10, pady=5)

            latime_rem_label = Label(self.frame_detalii_tehnice, text="Latime:")
            latime_rem_label.grid(row=1, column=2, sticky="w", padx=10, pady=5)

            latime_rem = Label(self.frame_detalii_tehnice, text=f"{detalii_rem[0][9]} m")
            latime_rem.grid(row=1, column=3, sticky="w", padx=10, pady=5)

            inaltime_rem_label = Label(self.frame_detalii_tehnice, text="Inaltime:")
            inaltime_rem_label.grid(row=2, column=2, sticky="w", padx=10, pady=5)

            inaltime_rem = Label(self.frame_detalii_tehnice, text=f"{detalii_rem[0][10]} m")
            inaltime_rem.grid(row=2, column=3, sticky="w", padx=10, pady=5)

            masa_max_rem_label = Label(self.frame_detalii_tehnice, text="Masa maxima admisa:")
            masa_max_rem_label.grid(row=3, column=2, sticky="w", padx=10, pady=5)

            masa_max_rem = Label(self.frame_detalii_tehnice, text=f"{detalii_rem[0][11]} kg")
            masa_max_rem.grid(row=3, column=3, sticky="w", padx=10, pady=5)

            incarcatura_max_rem_label = Label(self.frame_detalii_tehnice, text="Incarcatura maxima admisa:")
            incarcatura_max_rem_label.grid(row=4, column=2, sticky="w", padx=10, pady=5)

            incarcatura_max_rem = Label(self.frame_detalii_tehnice, text=f"{detalii_rem[0][12]} kg")
            incarcatura_max_rem.grid(row=4, column=3, sticky="w", padx=10, pady=5)

        else: 
            # self.frame_detalii_tehnice.grid_forget()
            for widget in self.frame_detalii_tehnice.winfo_children():
                widget.destroy()

            self.frame_detalii_tehnice.grid_forget()

            # self.frame_detalii_tehnice = LabelFrame(self.frame_detalii, text="Detalii Tehnice")
            # self.frame_detalii_tehnice.grid(row=0, column=1, padx=10, pady=10)

            # self.data_inmatriculare_label = Label(self.frame_detalii_tehnice, text="Data primei inmatriculari:")
            # self.data_inmatriculare_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

            # self.data_inmatriculare = Label(self.frame_detalii_tehnice, text="")
            # self.data_inmatriculare.grid(row=0, column=1, sticky="w", padx=10, pady=5)

            # self.serie_civ_label = Label(self.frame_detalii_tehnice, text="Serie CIV:")
            # self.serie_civ_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

            # self.serie_civ = Label(self.frame_detalii_tehnice, text="")
            # self.serie_civ.grid(row=1, column=1, sticky="w", padx=10, pady=5)

            # self.serie_talon_label = Label(self.frame_detalii_tehnice, text="Serie talon:")
            # self.serie_talon_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

            # self.serie_talon = Label(self.frame_detalii_tehnice, text="")
            # self.serie_talon.grid(row=2, column=1, sticky="w", padx=10, pady=5)

            # self.culoare_label = Label(self.frame_detalii_tehnice, text="Culoare:")
            # self.culoare_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

            # self.culoare = Label(self.frame_detalii_tehnice, text="")
            # self.culoare.grid(row=3, column=1, sticky="w", padx=10, pady=5)

            # tip_remorca_label = Label(self.frame_detalii_tehnice, text="Tip remorca:")
            # tip_remorca_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

            # tip_remorca = Label(self.frame_detalii_tehnice, text="")
            # tip_remorca.grid(row=4, column=1, sticky="w", padx=10, pady=5)

            # axe_label = Label(self.frame_detalii_tehnice, text="Numar axe:")
            # axe_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)

            # axe = Label(self.frame_detalii_tehnice, text="")
            # axe.grid(row=5, column=1, sticky="w", padx=10, pady=5)

            # lungime_rem_label = Label(self.frame_detalii_tehnice, text="Lungime:")
            # lungime_rem_label.grid(row=0, column=2, sticky="w", padx=10, pady=5)

            # lungime_rem = Label(self.frame_detalii_tehnice, text="")
            # lungime_rem.grid(row=0, column=3, sticky="w", padx=10, pady=5)

            # latime_rem_label = Label(self.frame_detalii_tehnice, text="Latime:")
            # latime_rem_label.grid(row=1, column=2, sticky="w", padx=10, pady=5)

            # latime_rem = Label(self.frame_detalii_tehnice, text="")
            # latime_rem.grid(row=1, column=3, sticky="w", padx=10, pady=5)

            # inaltime_rem_label = Label(self.frame_detalii_tehnice, text="Inaltime:")
            # inaltime_rem_label.grid(row=2, column=2, sticky="w", padx=10, pady=5)

            # inaltime_rem = Label(self.frame_detalii_tehnice, text="")
            # inaltime_rem.grid(row=2, column=3, sticky="w", padx=10, pady=5)

            # masa_max_rem_label = Label(self.frame_detalii_tehnice, text="Masa maxima admisa:")
            # masa_max_rem_label.grid(row=3, column=2, sticky="w", padx=10, pady=5)

            # masa_max_rem = Label(self.frame_detalii_tehnice, text="")
            # masa_max_rem.grid(row=3, column=3, sticky="w", padx=10, pady=5)

            # incarcatura_max_rem_label = Label(self.frame_detalii_tehnice, text="Incarcatura maxima admisa:")
            # incarcatura_max_rem_label.grid(row=4, column=2, sticky="w", padx=10, pady=5)

            # incarcatura_max_rem = Label(self.frame_detalii_tehnice, text="")
            # incarcatura_max_rem.grid(row=4, column=3, sticky="w", padx=10, pady=5)
        
        sql = "SELECT * FROM tabel_scadente WHERE id_tms = %s AND nume = %s"
        value = (id, date_rem[0])
        cursor.execute(sql, value)

        scadente = cursor.fetchall()

        print(scadente)

        self.scadente_frame = Frame(self.frame_detalii)
        self.scadente_frame.grid(row=0, column=2, pady=5, sticky="nw")

        Scadente(self.scadente_frame, id, date_rem[0], 'SEMIREMORCA')

        # if scadente:
        #     scadente_frame.grid_forget()
        #     scadente_frame.grid(row=0, column=2, rowspan=5, padx=10, pady=10, sticky="nw")

        #     for i, remorca in enumerate(scadente):
        #         # if "RCA" in str(remorca[4]):
        #         #     print(remorca)
        #         # print(f"{remorca[4]}: {remorca[5]}")
        #         # print(i)
        #         # print(remorca[5] - timedelta(days=15))
        #         if (date.today() + timedelta(days=15)) >= remorca[5] - timedelta(days=15):
        #             Label(scadente_frame, text=f"{remorca[4]}: {remorca[5]}", fg="red").grid(row=i, column=0, sticky="w", padx=10, pady=5)
        #         else:
        #             Label(scadente_frame, text=f"{remorca[4]}: {remorca[5]}", fg="green").grid(row=i, column=0, sticky="w", padx=10, pady=5)


        self.documente_frame = Frame(self.frame_detalii)
        self.documente_frame.grid(row=0, column=3, pady=5, sticky="nw")

        Documente(self.documente_frame, id, date_rem[0])

    def incarca_remorci(self):
        lista_remorci = []
        try:
            connection._open_connection()
            cursor.execute("SELECT * FROM tauros_truck WHERE categorie='SEMIREMORCA'")

        except:
            messagebox.messagebox.showerror(title="Connection error", message="Could not connect to DB Server")

        remorci = cursor.fetchall()
        connection.close()
        for remorca in remorci:
            self.remorca_table.insert('', 'end', text=str(remorca[0]), values=(remorca[1], remorca[5], remorca[2], remorca[6]))
            self.lista_remorci.append((remorca[0], remorca[1], remorca[5], remorca[2], remorca[6], remorca[8]))

        # return self.lista_remorci

    def cautare_remorci(self):
        remorci_list = self.lista_remorci
        query = self.remorca_plate.get()
        # for child in self.remorca_table.get_children():
        #     if query.lower() in str(self.remorca_table.item(child)['values']).lower():
        #         self.remorca_table.selection_set(child)
        #     else:
        #         self.remorca_table.selection_remove(child)

        self.remorca_table.delete(*self.remorca_table.get_children())
        for remorca in remorci_list:
            if query.lower() in str(remorca).lower():
                self.remorca_table.insert('', 'end', text=str(remorca[0]), values=(remorca[1], remorca[2], remorca[3], remorca[4]))


    def incarca_detalii(self, e):
        selected = self.remorca_table.focus()
        values = self.remorca_table.item(selected, 'values')
        id = self.remorca_table.item(selected, 'text')
        # Debug code
        # print(id)
        # print(values)
        # Golim frame-ul
        for widget in self.frame_detalii.winfo_children():
            widget.destroy()    
        self.frame_detalii.pack_forget()
        self.detalii_remorca(values, id)

if __name__ == "__main__":
    root = Tk()
    # root.title("Adaugare Vehicul")
    # root.geometry("900x600")  
    root.title("Gestionare Flota")
    root.geometry("1300x600")
    hello = Vehicule(root)

    root.mainloop()
