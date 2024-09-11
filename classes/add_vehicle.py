from tkinter import *
from tkinter import ttk, messagebox
from ttkwidgets.frames import ScrolledFrame
from requests import delete
# from tkinter.tix import ComboBox
from utils.tooltip import ToolTip
from liste import Remorci, Lista_clienti
from datetime import datetime, timedelta, date
from upload_download_docs import Documente
from scadente import Scadente
from PIL import Image, ImageTk
from right_click_menu import RightClickMenu
from tkcalendar import DateEntry
from ttkwidgets.autocomplete import AutocompleteCombobox
try:
    from database.datab import connection, cursor
except:
    mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server, program will exit")
    quit()

# TODO 
# - functie editare remorca - in progress
# - functie stergere remorca
# - funcie adaugare remorca
# - tab autovehicule
# - inventare remorci - in progress

class Vehicule:
    # modificarea vehiculelor
    def __init__(self, root):
        remorci = Remorci.afisare_remorci(root)
        self.root = root
        self.lista_remorci = []
        
        # self.main_frame = ttk.Notebook(self.root, width=1300, height=600)

        self.main_frame = ttk.Notebook(self.root)
        self.main_frame.pack(fill=BOTH, expand=1)

        self.frame_remorci()

    def frame_remorci(self):

        self.icon_modify_trailer = Image.open("classes/utils/icons/edit-pen-icon-18.jpg")
        self.icon_modify_trailer = self.icon_modify_trailer.resize((33, 33))
        self.icon_modify_trailer = ImageTk.PhotoImage(self.icon_modify_trailer)

        self.icon_reset_trailers = Image.open("classes/utils/icons/reverse-icon-png-20.jpg")
        self.icon_reset_trailers = self.icon_reset_trailers.resize((33, 33))
        self.icon_reset_trailers = ImageTk.PhotoImage(self.icon_reset_trailers)

        self.test_frame = ScrolledFrame(self.main_frame, compound=RIGHT)
        self.test_frame.pack(fill=BOTH, expand=1, anchor="center")

        # self.remorca_frame = Frame(self.main_frame)
        self.remorca_frame = Frame(self.test_frame.interior)
        self.remorca_frame.pack(fill=BOTH, expand=1, anchor="center")

        # self.main_frame.add(self.remorca_frame, text="Remorci")
        self.main_frame.add(self.test_frame, text="Remorci")

        self.vehicule_frame = LabelFrame(self.remorca_frame, text="Lista Semiremorci")
        self.vehicule_frame.pack()

        self.frame_cautare = Frame(self.vehicule_frame)
        self.frame_cautare.pack(pady=10, anchor=W)
        
        self.cautare_remorci_label = Label(self.frame_cautare, text="Cautare:")
        self.cautare_remorci_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        # self.remorca_plate = ttk.Combobox(self.vehicule_frame, values=remorci)
        self.remorca_plate = Entry(self.frame_cautare)
        self.remorca_plate.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        RightClickMenu.create_context_menu(self, self.remorca_plate)

        self.edit_remorca = Button(self.frame_cautare, image=self.icon_modify_trailer, borderwidth=0, highlightthickness=0, relief="flat", state="disabled", command=lambda:self.editare_remorca(self.id_remorca, self.date_remorca))
        self.edit_remorca.grid(row=0, column=2, sticky="e", padx=10, pady=10, ipadx=5, ipady=5)
        ToolTip(self.edit_remorca, "Editare")

        self.reset_remorci = Button(self.frame_cautare, image=self.icon_reset_trailers, borderwidth=0, highlightthickness=0, relief="flat", state="disabled", command=self.reset_detalii)
        self.reset_remorci.grid(row=0, column=3, sticky="e", padx=10, pady=10, ipadx=5, ipady=5)
        ToolTip(self.reset_remorci, "Resetare")

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
        self.frame_detalii.pack(padx=10, pady=5, anchor="center")

        # self.detalii_remorca()

    def detalii_remorca(self, date_rem, id):

        def incarca_inventare():
            try:
                connection._open_connection()
                sql = "SELECT * FROM inventar_remorci WHERE id_tms = %s"
                cursor.execute(sql, (id, ))

                inventare = cursor.fetchall()

            except:
                messagebox.showerror("Error", "Nu s-a putut conecta la baza de date!")

            if inventare:
                for i in range(len(inventare)):
                    print(inventare[i])
                    print(date_rem[0])
                    inv_remorca_tree.insert(parent='', index='end', iid=i, text='', values=(date_rem[0], inventare[i][0], inventare[i][2], inventare[i][3]))
        
        def reincarca_inventare():
            for i in inv_remorca_tree.get_children():
                inv_remorca_tree.delete(i)

            incarca_inventare()
            print("OK")

        self.date_remorca = date_rem
        self.id_remorca = id

        self.icon_modify = Image.open("classes/utils/icons/edit-pen-icon-18.jpg")
        self.icon_modify = self.icon_modify.resize((22, 22))
        self.icon_modify = ImageTk.PhotoImage(self.icon_modify)

        self.icon_add_new = Image.open("classes/utils/icons/add-text-icon-15.jpg")
        self.icon_add_new = self.icon_add_new.resize((22, 22))
        self.icon_add_new = ImageTk.PhotoImage(self.icon_add_new)

        self.frame_detalii = Frame(self.remorca_frame)

        self.frame_detalii.pack(padx=10, pady=10, anchor="center")

        self.detalii_tab = ttk.Notebook(self.frame_detalii)
        self.detalii_tab.grid(row=0, column=0, padx=2, pady=10)

        # self.frame_detalii_generale = LabelFrame(self.detalii_tab, text="Detalii Generale")
        self.frame_detalii_generale = Frame(self.detalii_tab)
        self.frame_detalii_generale.grid(row=0, column=0, padx=2, pady=10)

        self.detalii_tab.add(self.frame_detalii_generale, text="Generale")

        self.nr_auto_label = Label(self.frame_detalii_generale, text="Numar inmatriculare:")
        self.nr_auto_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.nr_auto = Label(self.frame_detalii_generale, text=date_rem[0])
        self.nr_auto.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        self.marca_label = Label(self.frame_detalii_generale, text="Marca:")
        self.marca_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.marca = Label(self.frame_detalii_generale, text=date_rem[1])
        self.marca.grid(row=1, column=1, sticky="w", padx=10, pady=5, columnspan=2)

        self.serie_sasiu_label = Label(self.frame_detalii_generale, text="Serie sasiu:")
        self.serie_sasiu_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.serie_sasiu = Label(self.frame_detalii_generale, text=date_rem[2])
        self.serie_sasiu.grid(row=2, column=1, sticky="w", padx=10, pady=5, columnspan=2)

        self.an_fabricatie_label = Label(self.frame_detalii_generale, text="An fabricatie:")
        self.an_fabricatie_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.an_fabricatie = Label(self.frame_detalii_generale, text=date_rem[3])
        self.an_fabricatie.grid(row=3, column=1, sticky="w", padx=10, pady=5, columnspan=2)

        self.id_label = Label(self.frame_detalii_generale, text="ID TMS:")
        self.id_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        self.id = Label(self.frame_detalii_generale, text=id)
        self.id.grid(row=4, column=1, sticky="w", padx=10, pady=5, columnspan=2)

        
        for remorca in self.lista_remorci:
            if str(id) == str(remorca[0]):
                self.edit_remorca.configure(state="normal")
                self.reset_remorci.configure(state="normal")

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

        
        # self.frame_detalii_tehnice = LabelFrame(self.detalii_tab, text="Detalii Tehnice")
        self.frame_detalii_tehnice = Frame(self.detalii_tab)
        self.frame_detalii_tehnice.grid(row=0, column=0, padx=2, pady=5)

        self.detalii_tab.add(self.frame_detalii_tehnice, text="Detalii Tehnice")

        if len(detalii_rem) > 0:
        #     self.frame_detalii_tehnice.grid_forget()
        #     self.frame_detalii_tehnice.grid(row=0, column=0, padx=10, pady=10)
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

        # else: 
        #     # self.frame_detalii_tehnice.grid_forget()
        #     for widget in self.frame_detalii_tehnice.winfo_children():
        #         widget.destroy()

        #     self.frame_detalii_tehnice.grid_forget()

        self.frame_inventare_remorci = Frame(self.detalii_tab)
        self.frame_inventare_remorci.grid(row=0, column=0, padx=2, pady=5)

        self.detalii_tab.add(self.frame_inventare_remorci, text="Inventare")

        frame_tabel_inventare = Frame(self.frame_inventare_remorci)
        frame_tabel_inventare.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="nesw")

        # Scrollbar pentru treeview inventare remorci
        inv_remorca_scroll = Scrollbar(frame_tabel_inventare)
        inv_remorca_scroll.pack(side=RIGHT, fill=Y)

        # cream tabelul
        inv_remorca_tree = ttk.Treeview(frame_tabel_inventare, yscrollcommand=inv_remorca_scroll.set, selectmode="extended", height=5)

        # Definire coloane
        inv_remorca_tree['columns'] = ("Nr. remorca", "Nr. inventar", "Data inventar", "Intocmit de")

        # Formatare coloane
        inv_remorca_tree.column("#0", width=0, stretch=NO)
        inv_remorca_tree.column("Nr. remorca", anchor=CENTER, width=100)
        inv_remorca_tree.column("Nr. inventar", anchor=CENTER, width=100)
        inv_remorca_tree.column("Data inventar", anchor=CENTER, width=100)
        inv_remorca_tree.column("Intocmit de", anchor=CENTER, width=100)

        # Heading
        inv_remorca_tree.heading("#0", text="", anchor=CENTER)
        inv_remorca_tree.heading("Nr. remorca", text="Nr. remorca", anchor=CENTER)
        inv_remorca_tree.heading("Nr. inventar", text="Nr. inventar", anchor=CENTER)
        inv_remorca_tree.heading("Data inventar", text="Data inventar", anchor=CENTER)
        inv_remorca_tree.heading("Intocmit de", text="Intocmit de", anchor=CENTER)

        # # Adaugare date in tabel
        # for i in range(len(inventare_remorci)):
        #     inv_remorca_tree.insert(parent='', index='end', iid=i, text='', values=(inventare_remorci[i][0], inventare_remorci[i][1], inventare_remorci[i][2]))

        inv_remorca_tree.pack(side="left", fill="both", expand=True)

        # Confirgurare scrollbar
        inv_remorca_scroll.config(command=inv_remorca_tree.yview)

        incarca_inventare()

        # Adaugam butoane

        inventar_butoane_frame = Frame(self.frame_inventare_remorci)
        inventar_butoane_frame.grid(row=0, column=2, padx=10, pady=10)

        self.icon_refresh_inv = Image.open("classes/utils/icons/reset-icon-png-10.jpg")
        self.icon_refresh_inv = self.icon_refresh_inv.resize((22, 22))
        self.icon_refresh_inv = ImageTk.PhotoImage(self.icon_refresh_inv)

        inventar_nou_button = Button(inventar_butoane_frame, text="Inventar nou", image=self.icon_add_new, borderwidth=0, highlightthickness=0, relief="flat", command=lambda:self.adauga_inventar(id, date_rem[0]))
        inventar_nou_button.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        ToolTip(inventar_nou_button, 'Inventar nou')

        refresh_inventare = Button(inventar_butoane_frame, text="Refresh", image=self.icon_refresh_inv, borderwidth=0, highlightthickness=0, relief="flat", command=reincarca_inventare)
        refresh_inventare.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        ToolTip(refresh_inventare, 'Actualizare')

        
        # sql = "SELECT * FROM tabel_scadente WHERE id_tms = %s AND nume = %s"
        # value = (id, date_rem[0])
        # cursor.execute(sql, value)

        # scadente = cursor.fetchall()

        # print(scadente)

        self.scadente_frame = Frame(self.frame_detalii)
        self.scadente_frame.grid(row=0, column=2, pady=5, sticky="nw")

        Scadente(self.scadente_frame, id, date_rem[0], 'SEMIREMORCA')

        self.documente_frame = Frame(self.frame_detalii)
        self.documente_frame.grid(row=0, column=3, pady=5, sticky="nw")

        Documente(self.documente_frame, id, date_rem[0])

    def editare_remorca(self, id, numar):
        print(id)
        def salvare_modificari():
            
            try:
                connection._open_connection()
                sql = "UPDATE tauros_truck SET plate_no = %s, serie_sasiu = %s, marca = %s, an_fabricatie = %s, proprietar = %s WHERE truck_id = %s AND categorie = %s"
                values = (edit_nr_auto_entry.get().upper(), \
                        edit_serie_sasiu_entry.get().upper(), \
                        edit_marca_entry.get().upper(), \
                        edit_an_fabricatie_entry.get(), \
                        proprietar_combobox.get(), \
                        id, 'SEMIREMORCA')
                
                cursor.execute(sql, values)
                connection.commit()
                messagebox.showinfo(title="Success", message="Remorca modificata cu succes!")

            except:
                messagebox.showerror(title="Error", message="Eroare la modificare!")
            finally:
                connection.close()

            self.reset_detalii()
            edit_remorca_window.destroy()

        def salvare_date_tehnice():
            pass

        def incarcare_date_tehnice():
            try:
                connection._open_connection()
                sql = "SELECT * FROM date_tehnice_rem WHERE id_rem=%s"

                cursor.execute(sql, (id, ))

                result = cursor.fetchall()

                # print(result)
            except:
                messagebox.showerror(title="Error", message="Eroare la incarcare date tehnice!")

            finally:
                connection.close()

            return result

        edit_remorca_window = Toplevel(self.root)
        edit_remorca_window.transient(self.root)
        edit_remorca_window.grab_set()

        edit_remorca_notebook = ttk.Notebook(edit_remorca_window)
        edit_remorca_notebook.pack(expand=1, fill="both", padx=5, pady=5)

        edit_detalii_generale_tab = Frame(edit_remorca_notebook)
        edit_remorca_notebook.add(edit_detalii_generale_tab, text="Detalii generale")

        edit_detalii_generale_frame = LabelFrame(edit_detalii_generale_tab, text=f"Editare detalii generale {numar[0]}")
        edit_detalii_generale_frame.pack(expand=1, fill="both", padx=5, pady=5)

        clienti = Lista_clienti(edit_detalii_generale_frame).incarca_clienti()

        edit_nr_auto_label = Label(edit_detalii_generale_frame, text="Numar inmatriculare:")
        edit_nr_auto_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        edit_nr_auto_entry = Entry(edit_detalii_generale_frame)
        edit_nr_auto_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        edit_nr_auto_entry.insert(0, numar[0])

        edit_marca_label = Label(edit_detalii_generale_frame, text="Marca:")
        edit_marca_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        edit_marca_entry = Entry(edit_detalii_generale_frame)
        edit_marca_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        edit_marca_entry.insert(0, numar[1])

        edit_serie_sasiu_label = Label(edit_detalii_generale_frame, text="Serie sasiu:")
        edit_serie_sasiu_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        edit_serie_sasiu_entry = Entry(edit_detalii_generale_frame)
        edit_serie_sasiu_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        edit_serie_sasiu_entry.insert(0, numar[2])

        edit_an_fabricatie_label = Label(edit_detalii_generale_frame, text="An fabricatie:")
        edit_an_fabricatie_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        edit_an_fabricatie_entry = Entry(edit_detalii_generale_frame)
        edit_an_fabricatie_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        edit_an_fabricatie_entry.insert(0, numar[3])

        edit_proprietar_label = Label(edit_detalii_generale_frame, text="Proprietar:")
        edit_proprietar_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        
        proprietar = StringVar()

        proprietar_combobox = ttk.Combobox(edit_detalii_generale_frame, textvariable=proprietar, values=clienti)
        proprietar_combobox.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        butoane_modificare_remorca_frame = Frame(edit_detalii_generale_frame)
        butoane_modificare_remorca_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.salvare_mod_remorca_button = Button(butoane_modificare_remorca_frame, text="Salveaza", command=salvare_modificari)
        self.salvare_mod_remorca_button.grid(row=0, column=0, padx=10, pady=5)

        self.anulare_mod_remorca_button = Button(butoane_modificare_remorca_frame, text="Anuleaza", command=edit_remorca_window.destroy)
        self.anulare_mod_remorca_button.grid(row=0, column=1, padx=10, pady=5)

        date_tehnice = incarcare_date_tehnice()

        # Cautam remorca in lista si extragem proprietarul. 

        for remorca in self.lista_remorci:
            if str(remorca[0]) == str(id):
                # print(remorca[5])
                proprietar = str(remorca[5])

            # else:
            #     proprietar = ""

            proprietar_combobox.set(proprietar)

        edit_detalii_tehnice_tab = Frame(edit_remorca_notebook)
        edit_remorca_notebook.add(edit_detalii_tehnice_tab, text="Detalii tehnice")

        edit_detalii_tehnice_frame = LabelFrame(edit_detalii_tehnice_tab, text=f"Editare detalii tehnice {numar[0]}")
        edit_detalii_tehnice_frame.pack(expand=1, fill="both", padx=5, pady=5)

        data_inmatriculare_remorca_label = Label(edit_detalii_tehnice_frame, text="Data primei inmatriculari:")
        data_inmatriculare_remorca_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        data_inmatriculare_remorca_entry = DateEntry(edit_detalii_tehnice_frame, locale="RO_ro", date_pattern='yyyy-MM-dd', width=17)
        data_inmatriculare_remorca_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        lungime_remorca_label = Label(edit_detalii_tehnice_frame, text="Lungime:")
        lungime_remorca_label.grid(row=0, column=2, sticky="w", padx=10, pady=5)

        lungime_remorca_entry = Entry(edit_detalii_tehnice_frame)
        lungime_remorca_entry.grid(row=0, column=3, padx=10, pady=5, sticky="w")

        serie_civ_remorca_label = Label(edit_detalii_tehnice_frame, text="Serie CIV:")
        serie_civ_remorca_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        serie_civ_remorca_entry = Entry(edit_detalii_tehnice_frame)
        serie_civ_remorca_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        latime_remorca_label = Label(edit_detalii_tehnice_frame, text="Latime:")
        latime_remorca_label.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        latime_remorca_entry = Entry(edit_detalii_tehnice_frame)
        latime_remorca_entry.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        serie_talon_remorca_label = Label(edit_detalii_tehnice_frame, text="Serie talon:")
        serie_talon_remorca_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        serie_talon_remorca_entry = Entry(edit_detalii_tehnice_frame)
        serie_talon_remorca_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        inaltime_remorca_label = Label(edit_detalii_tehnice_frame, text="Inaltime:")
        inaltime_remorca_label.grid(row=2, column=2, sticky="w", padx=10, pady=5)

        inaltime_remorca_entry = Entry(edit_detalii_tehnice_frame)
        inaltime_remorca_entry.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        culoare_remorca_label = Label(edit_detalii_tehnice_frame, text="Culoare:")
        culoare_remorca_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        culoare_remorca_entry = Entry(edit_detalii_tehnice_frame)
        culoare_remorca_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        masa_maxima_admisa_label = Label(edit_detalii_tehnice_frame, text="Masa maxima admisa (Kg):")
        masa_maxima_admisa_label.grid(row=3, column=2, sticky="w", padx=10, pady=5)

        masa_maxima_admisa_entry = Entry(edit_detalii_tehnice_frame)
        masa_maxima_admisa_entry.grid(row=3, column=3, padx=10, pady=5, sticky="w")
        
        tip_remorca_label = Label(edit_detalii_tehnice_frame, text="Tip remorca:")
        tip_remorca_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        tip_remorca_entry = ttk.Combobox(edit_detalii_tehnice_frame, values=["Prelata", "Platforma"], width=17)
        tip_remorca_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        incarcatura_max_admisa_label = Label(edit_detalii_tehnice_frame, text="Incarcatura maxima admisa (Kg):")
        incarcatura_max_admisa_label.grid(row=4, column=2, sticky="w", padx=10, pady=5)

        incarcatura_max_admisa_entry = Entry(edit_detalii_tehnice_frame)
        incarcatura_max_admisa_entry.grid(row=4, column=3, padx=10, pady=5, sticky="w")

        numar_axe_label = Label(edit_detalii_tehnice_frame, text="Numar axe:")
        numar_axe_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)

        numar_axe_entry = Entry(edit_detalii_tehnice_frame)
        numar_axe_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Verificam daca exista datele tehnice in db si le incarcam. 
        if date_tehnice:
            data_inmatriculare_remorca_entry.set_date(date_tehnice[0][2])
            lungime_remorca_entry.insert(0, str(date_tehnice[0][8]))
            serie_civ_remorca_entry.insert(0, str(date_tehnice[0][3]))
            latime_remorca_entry.insert(0, str(date_tehnice[0][9]))
            serie_talon_remorca_entry.insert(0, str(date_tehnice[0][4]))
            inaltime_remorca_entry.insert(0, str(date_tehnice[0][10]))
            culoare_remorca_entry.insert(0, str(date_tehnice[0][5]))
            masa_maxima_admisa_entry.insert(0, str(date_tehnice[0][11]))
            tip_remorca_entry.set(str(date_tehnice[0][13]))
            incarcatura_max_admisa_entry.insert(0, str(date_tehnice[0][12]))
            numar_axe_entry.insert(0, str(date_tehnice[0][7]))
        
    def adauga_remorca(self):
        pass

    def adauga_inventar(self, id, nr_remorca, id_inv=None):
        print(id, nr_remorca)

        data_inventar = date.today().strftime("%Y-%m-%d")
        # print(data_inventar)

        # Introducem un inventar nou in baza de date. 
        def inventar_nou():
            disable_fields()
            try:
                connection._open_connection()

            except:
                messagebox.showerror("Error", "Nu s-a putut conecta la baza de date!")

            else:
                sql = "INSERT INTO inventar_remorci (id_tms, data_inventar, intocmit, axa1_marca, axa1_dim, axa1_stare, axa2_marca, axa2_dim, axa2_stare, axa3_marca, axa3_dim, axa3_stare, \
                    rezerva_cap, rezerva_rem, cablu_vamal, coltare, covorase, stickere, scanduri, chingi, clicheti, bari, cala, stiker_unghi) \
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (id, data_inventar_entry.get(), \
                            intocmit_de_entry.get(), \
                            marca_anv_axa1_entry.get(), \
                            dim_anv_axa1_entry.get(), \
                            stare_anv_axa1_entry.get(), \
                            marca_anv_axa2_entry.get(), \
                            dim_anv_axa2_entry.get(), \
                            stare_anv_axa2_entry.get(), \
                            marca_anv_axa3_entry.get(), \
                            dim_anv_axa3_entry.get(), \
                            stare_anv_axa3_entry.get(), \
                            rezerva_cap_var.get(), \
                            rezerva_remorca_var.get(), \
                            cablu_vamal_var.get(), \
                            coltare_var.get(), \
                            covorase_var.get(), \
                            sticker_limite_var.get(), \
                            nr_scanduri_entry.get(), \
                            nr_chingi_entry.get(), \
                            nr_crikete_entry.get(), \
                            nr_bari_marfa_entry.get(), \
                            nr_cala_roata_entry.get(), \
                            nr_stickere_unghi_entry.get())
                
                cursor.execute(sql, values)
                connection.commit()

                sql = "SELECT id from inventar_remorci WHERE id_tms = %s ORDER BY id DESC LIMIT 1"

                cursor.execute(sql, (id,))

                result = cursor.fetchall()
                id_inv = result[0][0]

                nr_inventar_entry.config(state="normal")

                nr_inventar_entry.insert(0, id_inv)

                nr_inventar_entry.config(state="disabled")

                connection.close()

                messagebox.showinfo("Success", "Inventar adaugat cu succes!")

                file_menu.entryconfig(0, state="active")
                file_menu.entryconfig(1, state="active")
                file_menu.entryconfig(2, state="disabled")
        

        def disable_fields():
            data_inventar_entry.config(state="disabled")
            intocmit_de_entry.config(state="disabled")
            marca_anv_axa1_entry.config(state="disabled")
            dim_anv_axa1_entry.config(state="disabled")
            stare_anv_axa1_entry.config(state="disabled")
            marca_anv_axa2_entry.config(state="disabled")
            dim_anv_axa2_entry.config(state="disabled")
            stare_anv_axa2_entry.config(state="disabled")
            marca_anv_axa3_entry.config(state="disabled")
            dim_anv_axa3_entry.config(state="disabled")
            stare_anv_axa3_entry.config(state="disabled")
            rezerva_cap_check.config(state="disabled")
            rezerva_remorca_check.config(state="disabled")
            cablu_vamal_check.config(state="disabled")
            coltare_check.config(state="disabled")
            covorase_check.config(state="disabled")
            sticker_limite_check.config(state="disabled")
            nr_scanduri_entry.config(state="disabled")
            nr_chingi_entry.config(state="disabled")
            nr_crikete_entry.config(state="disabled")
            nr_bari_marfa_entry.config(state="disabled")
            nr_cala_roata_entry.config(state="disabled")
            nr_stickere_unghi_entry.config(state="disabled")

            file_menu.entryconfig(0, state="active")
            file_menu.entryconfig(1, state="active")
            file_menu.entryconfig(2, state="disabled")

        def enable_fields():
            data_inventar_entry.config(state="normal")
            intocmit_de_entry.config(state="normal")
            marca_anv_axa1_entry.config(state="normal")
            dim_anv_axa1_entry.config(state="normal")
            stare_anv_axa1_entry.config(state="normal")
            marca_anv_axa2_entry.config(state="normal")
            dim_anv_axa2_entry.config(state="normal")
            stare_anv_axa2_entry.config(state="normal")
            marca_anv_axa3_entry.config(state="normal")
            dim_anv_axa3_entry.config(state="normal")
            stare_anv_axa3_entry.config(state="normal")
            rezerva_cap_check.config(state="normal")
            rezerva_remorca_check.config(state="normal")
            cablu_vamal_check.config(state="normal")
            coltare_check.config(state="normal")
            covorase_check.config(state="normal")
            sticker_limite_check.config(state="normal")
            nr_scanduri_entry.config(state="normal")
            nr_chingi_entry.config(state="normal")
            nr_crikete_entry.config(state="normal")
            nr_bari_marfa_entry.config(state="normal")
            nr_cala_roata_entry.config(state="normal")
            nr_stickere_unghi_entry.config(state="normal")

        def clear_fields():
            enable_fields()
            data_inventar_entry.set_date(data_inventar)
            intocmit_de_entry.delete(0, END)
            marca_anv_axa1_entry.delete(0, END)
            dim_anv_axa1_entry.delete(0, END)
            stare_anv_axa1_entry.delete(0, END)
            marca_anv_axa2_entry.delete(0, END)
            dim_anv_axa2_entry.delete(0, END)
            stare_anv_axa2_entry.delete(0, END)
            marca_anv_axa3_entry.delete(0, END)
            dim_anv_axa3_entry.delete(0, END)
            stare_anv_axa3_entry.delete(0, END)
            rezerva_cap_check.deselect()
            rezerva_remorca_check.deselect()
            cablu_vamal_check.deselect()
            coltare_check.deselect()
            covorase_check.deselect()
            sticker_limite_check.deselect()
            nr_scanduri_entry.delete(0, END)
            nr_chingi_entry.delete(0, END)
            nr_crikete_entry.delete(0, END)
            nr_bari_marfa_entry.delete(0, END)
            nr_cala_roata_entry.delete(0, END)
            nr_stickere_unghi_entry.delete(0, END)

            file_menu.entryconfig(0, state="disabled")
            file_menu.entryconfig(1, state="disabled")
            file_menu.entryconfig(2, state="active")
        
        def edit_inventar():
            enable_fields()
            file_menu.entryconfig(0, state="active")
            file_menu.entryconfig(1, state="disabled")
            file_menu.entryconfig(2, state="active")
        

        lista_angajati = []

        connection._open_connection()
        sql = "SELECT nume, prenume from angajati"
        cursor.execute(sql)
        angajati = cursor.fetchall()
        connection.close()

        for nume, prenume in angajati:
            lista_angajati.append(f"{prenume} {nume}")

        stare_anvelopa = ["Noi", "Uzate", "Pana stanga", "Pana dreapta", "Schimb stanga", "Schimb dreapta", "Schimb ambele"]

        adauga_inventar_window = Toplevel(self.root)
        adauga_inventar_window.title("Adaugare inventar")
        adauga_inventar_window.transient(self.root)
        adauga_inventar_window.grab_set()

        menubar = Menu(adauga_inventar_window)
        adauga_inventar_window.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Nou", accelerator="Ctrl+N", command=clear_fields)
        file_menu.add_command(label="Editeaza", accelerator="Ctrl+E", command=edit_inventar)
        file_menu.add_command(label="Salveaza", accelerator="Ctrl+S", command=inventar_nou)
        file_menu.add_separator()
        file_menu.add_command(label="Inchide", command=adauga_inventar_window.destroy)
        menubar.add_cascade(label="Fisier", menu=file_menu, underline=0)

        file_menu.entryconfig("Editeaza", state="disabled")
        file_menu.entryconfig("Nou", state="disabled")

        adauga_inventar_frame = LabelFrame(adauga_inventar_window, text=f"Adaugare inventar {nr_remorca}")
        adauga_inventar_frame.pack(expand=1, fill="both", padx=5, pady=5)

        nr_inventar_label = Label(adauga_inventar_frame, text="Nr. inventar:")
        nr_inventar_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        nr_inventar_entry = Entry(adauga_inventar_frame, state="readonly")
        nr_inventar_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        data_inventar_label = Label(adauga_inventar_frame, text="Data inventar:")
        data_inventar_label.grid(row=0, column=2, sticky="w", padx=10, pady=5)

        data_inventar_entry = DateEntry(adauga_inventar_frame, locale="RO_ro", date_pattern='yyyy-MM-dd')
        data_inventar_entry.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        data_inventar_entry.set_date(data_inventar)

        intocmit_de_label = Label(adauga_inventar_frame, text="Intocmit de:")
        intocmit_de_label.grid(row=0, column=4, padx=10, pady=5, sticky="w")

        intocmit_de_entry = AutocompleteCombobox(adauga_inventar_frame, completevalues=lista_angajati)
        intocmit_de_entry.grid(row=0, column=5, padx=10, pady=5, sticky="w")

        anv_axa_1_frame = LabelFrame(adauga_inventar_frame, text="Anvelope axa 1")
        anv_axa_1_frame.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        marca_anv_axa1_label = Label(anv_axa_1_frame, text="Marca:")
        marca_anv_axa1_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        marca_anv_axa1_entry = Entry(anv_axa_1_frame)
        marca_anv_axa1_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        dim_anv_axa1_label = Label(anv_axa_1_frame, text="Dimensiuni:")
        dim_anv_axa1_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        dim_anv_axa1_entry = Entry(anv_axa_1_frame)
        dim_anv_axa1_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        stare_anv_axa1_label = Label(anv_axa_1_frame, text="Stare anvelope:")
        stare_anv_axa1_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        stare_anv_axa1_entry = ttk.Combobox(anv_axa_1_frame, values=stare_anvelopa, width=17)
        stare_anv_axa1_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        anv_axa_2_frame = LabelFrame(adauga_inventar_frame, text="Anvelope axa 2")
        anv_axa_2_frame.grid(row=1, column=2, columnspan=2, sticky="w", padx=10, pady=5)

        marca_anv_axa2_label = Label(anv_axa_2_frame, text="Marca:")
        marca_anv_axa2_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        marca_anv_axa2_entry = Entry(anv_axa_2_frame)
        marca_anv_axa2_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        dim_anv_axa2_label = Label(anv_axa_2_frame, text="Dimensiuni:")
        dim_anv_axa2_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        dim_anv_axa2_entry = Entry(anv_axa_2_frame)
        dim_anv_axa2_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        stare_anv_axa2_label = Label(anv_axa_2_frame, text="Stare anvelope:")
        stare_anv_axa2_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        stare_anv_axa2_entry = ttk.Combobox(anv_axa_2_frame, values=stare_anvelopa, width=17)
        stare_anv_axa2_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        anv_axa_3_frame = LabelFrame(adauga_inventar_frame, text="Anvelope axa 3")
        anv_axa_3_frame.grid(row=1, column=4, columnspan=2, sticky="w", padx=10, pady=5)

        marca_anv_axa3_label = Label(anv_axa_3_frame, text="Marca:")
        marca_anv_axa3_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        marca_anv_axa3_entry = Entry(anv_axa_3_frame)
        marca_anv_axa3_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        dim_anv_axa3_label = Label(anv_axa_3_frame, text="Dimensiuni:")
        dim_anv_axa3_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        dim_anv_axa3_entry = Entry(anv_axa_3_frame)
        dim_anv_axa3_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        stare_anv_axa3_label = Label(anv_axa_3_frame, text="Stare anvelope:")
        stare_anv_axa3_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        stare_anv_axa3_entry = ttk.Combobox(anv_axa_3_frame, values=stare_anvelopa, width=17)
        stare_anv_axa3_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        dotari_remorca_frame = LabelFrame(adauga_inventar_frame, text="Dotari remorca")
        dotari_remorca_frame.grid(row=2, column=0, columnspan=6, sticky="ew", padx=10, pady=5)

        check_button_frame = Frame(dotari_remorca_frame)
        check_button_frame.pack(padx=5, pady=5, expand=True)



        rezerva_cap_var = IntVar()
        
        rezerva_cap_check = Checkbutton(check_button_frame, text="Rezerva cap tractor", variable=rezerva_cap_var)
        rezerva_cap_check.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        rezerva_remorca_var = IntVar()

        rezerva_remorca_check = Checkbutton(check_button_frame, text="Rezerva remorca", variable=rezerva_remorca_var)
        rezerva_remorca_check.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        cablu_vamal_var = IntVar()

        cablu_vamal_check = Checkbutton(check_button_frame, text="Cablu Vamal", variable=cablu_vamal_var)
        cablu_vamal_check.grid(row=0, column=2, sticky="w", padx=5, pady=5)

        coltare_var = IntVar()

        coltare_check = Checkbutton(check_button_frame, text="Coltare", variable=coltare_var)
        coltare_check.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        covorase_var = IntVar()

        covorase_check = Checkbutton(check_button_frame, text="Covorase", variable=covorase_var)
        covorase_check.grid(row=0, column=4, sticky="w", padx=5, pady=5)

        sticker_limite_var = IntVar()

        sticker_limite_check = Checkbutton(check_button_frame, text="Stickere limite viteza", variable=sticker_limite_var)
        sticker_limite_check.grid(row=0, column=5, sticky="w", padx=5, pady=5)

        echipare_remorca_frame = Frame(dotari_remorca_frame)
        echipare_remorca_frame.pack(padx=5, pady=5)

        nr_scanduri_label = Label(echipare_remorca_frame, text="Nr. scanduri:")
        nr_scanduri_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        nr_scanduri_entry = Entry(echipare_remorca_frame)
        nr_scanduri_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        nr_chingiri_label = Label(echipare_remorca_frame, text="Nr. chingi:")
        nr_chingiri_label.grid(row=0, column=2, sticky="w", padx=5, pady=5)

        nr_chingi_entry = Entry(echipare_remorca_frame)
        nr_chingi_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        nr_crikete_label = Label(echipare_remorca_frame, text="Nr. clicheti:")
        nr_crikete_label.grid(row=0, column=4, sticky="w", padx=5, pady=5)

        nr_crikete_entry = Entry(echipare_remorca_frame)
        nr_crikete_entry.grid(row=0, column=5, padx=5, pady=5, sticky="w")

        nr_bari_marfa_label = Label(echipare_remorca_frame, text="Nr. bari marfa:")
        nr_bari_marfa_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        nr_bari_marfa_entry = Entry(echipare_remorca_frame)
        nr_bari_marfa_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        nr_cala_roata_label = Label(echipare_remorca_frame, text="Cala roata:")
        nr_cala_roata_label.grid(row=1, column=2, sticky="w", padx=5, pady=5)

        nr_cala_roata_entry = Entry(echipare_remorca_frame)
        nr_cala_roata_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        nr_stickere_unghi_label = Label(echipare_remorca_frame, text="Stickere unghi:")
        nr_stickere_unghi_label.grid(row=1, column=4, sticky="w", padx=5, pady=5)

        nr_stickere_unghi_entry = Entry(echipare_remorca_frame)
        nr_stickere_unghi_entry.grid(row=1, column=5, padx=5, pady=5, sticky="w")




    def incarca_remorci(self):

        # Se incarca remorcile din baza de date si se populeaza treeview. 
        self.lista_remorci = []
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

        self.remorca_table.delete(*self.remorca_table.get_children())
        for remorca in remorci_list:
            if query.lower() in str(remorca).lower():
                self.remorca_table.insert('', 'end', text=str(remorca[0]), values=(remorca[1], remorca[2], remorca[3], remorca[4]))


    def incarca_detalii(self, e=None):
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

    def reset_detalii(self):
        """Resetam detaliile incarcate despre remorci, cautarea si butoanele."""
        self.lista_remorci = []
        for i in self.remorca_table.get_children():
            self.remorca_table.delete(i)

        self.incarca_remorci()

        self.remorca_plate.delete(0, END)
        for widget in self.frame_detalii.winfo_children():
            widget.destroy()
        self.frame_detalii.pack_forget()

        self.edit_remorca.configure(state="disabled")
        self.reset_remorci.configure(state="disabled")


if __name__ == "__main__":
    root = Tk()
    # root.title("Adaugare Vehicul")
    # root.geometry("900x600")  
    root.title("Gestionare Flota")
    # root.geometry("1300x600")
    hello = Vehicule(root)

    root.mainloop()
