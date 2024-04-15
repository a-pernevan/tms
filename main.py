# import add_client
from tkinter import *
from tkinter import ttk
from classes.clients import Clients
from classes.liste import Functii
root = Tk()
root.title("TMS Project 2024")
# root.geometry("900x600")

def refresh_window(root):
    global functii
    global lista_functii
    window = Toplevel(root)
    hello.adauga_functie(window)
    window.wait_window()
    # window.wait_window()
    print(type(window))
    
    # Redraw the window
    root.update()
    root.update_idletasks()
    lista_functii = hello.afisare_functii()
    functii.configure(values=lista_functii)
    print(lista_functii)
    


# hello = Clients(root)
hello = Functii(root)

lista_functii = hello.afisare_functii()

functii = ttk.Combobox(root, value=lista_functii)
functii.current(0)
functii.pack()
print(hello.afisare_functii())

functie_noua = Button(root, text="Adauga nou", command=lambda: refresh_window(root))
functie_noua.pack()




# add_client

root.mainloop()