# import add_client
from tkinter import *
from tkinter import ttk
from classes.clients import Clients
from classes.liste import Functii

root = Tk()
root.title("TMS Project 2024")
# root.geometry("900x600")

def refresh_window():
    hello.adauga_functie(root)
    # Redraw the window
    root.update()
    root.update_idletasks()
    functii.configure(values=hello.afisare_functii())
    


# hello = Clients(root)
hello = Functii(root)

functii = ttk.Combobox(root, value=hello.afisare_functii())
functii.current(0)
functii.pack()
print(hello.afisare_functii())

functie_noua = Button(root, text="Adauga nou", command= refresh_window)
functie_noua.pack()




# add_client

root.mainloop()