from cProfile import label
from tkinter import *
from tkinter import ttk, messagebox
from turtle import width
# from tkinter.tix import ComboBox
from liste import Remorci
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
        
        
        self.main_frame = ttk.Notebook(self.root, width=1200, height=600)
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

        self.frame_detalii = LabelFrame(self.remorca_frame, text="Detalii Remorca")
        self.frame_detalii.pack(padx=10, pady=10, anchor=W)

        # self.detalii_remorca()

    def detalii_remorca(self, date_rem, id):

        self.frame_detalii.pack(padx=10, pady=10, anchor=W)

        self.nr_auto_label = Label(self.frame_detalii, text="Numar inmatriculare:")
        self.nr_auto_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.nr_auto = Label(self.frame_detalii, text=date_rem[0])
        self.nr_auto.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        self.marca_label = Label(self.frame_detalii, text="Marca:")
        self.marca_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.marca = Label(self.frame_detalii, text=date_rem[1])
        self.marca.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        self.serie_sasiu_label = Label(self.frame_detalii, text="Serie sasiu:")
        self.serie_sasiu_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.serie_sasiu = Label(self.frame_detalii, text=date_rem[2])
        self.serie_sasiu.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        self.an_fabricatie_label = Label(self.frame_detalii, text="An fabricatie:")
        self.an_fabricatie_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.an_fabricatie = Label(self.frame_detalii, text=date_rem[3])
        self.an_fabricatie.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        self.id_label = Label(self.frame_detalii, text="ID TMS:")
        self.id_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        self.id = Label(self.frame_detalii, text=id)
        self.id.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        remorci = self.incarca_remorci()
        
        for remorca in remorci:
            if str(id) == str(remorca[0]):
                print(remorca)

        

        

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
            lista_remorci.append((remorca[0], remorca[1], remorca[5], remorca[2], remorca[6], remorca[8]))

        return lista_remorci

    def cautare_remorci(self):
        remorci_list = self.incarca_remorci()
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
        print(id)
        print(values)
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
