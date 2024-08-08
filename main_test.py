# import add_client
from tkinter import *
from tkinter import ttk
# from classes.clients import Clients
from classes import registru_parcare
from classes.liste import Functii, Filiala
root = Tk()
root.title("TMS Project 2024")
# root.geometry("900x600")

def refresh_window_functii(root):
    global functii
    global lista_functii
    # Cream o instanta noua si se trimite la class 
    window = Toplevel(root)
    # Se blocheaza fereastra mama pana se inchide fereastra de inroducere functie
    window.transient(root)
    window.grab_set()
    hello.adauga_functie(window)
    window.wait_window()
    
    # Redraw the window
    root.update()
    root.update_idletasks()
    lista_functii = hello.afisare_functii()
    functii.configure(values=lista_functii)
    print(lista_functii)
    


# hello = Clients(root)
hello = Functii(root)
sediu = Filiala(root)

parcare = registru_parcare.Registru_parcare(root)


lista_functii = hello.afisare_functii()
# Verificam daca exista inregistrari, in caz contrar adaugam una noua.
if lista_functii:

    functii = ttk.Combobox(root, value=lista_functii)
    functii.current(0)
    functii.bind("<Double-1>", lambda event: refresh_window_functii(root))
    functii.pack()
    

    # functie_noua = Button(root, text="Adauga nou", command=lambda: refresh_window(root))
    # functie_noua.pack()

else:
    window = Toplevel(root)
    hello.adauga_functie(window)



# add_client

lista_filiale = sediu.afisare_filiale()
print(lista_filiale)

# Verificam daca exista inregistrari, in caz contrar adaugam una noua.

if not lista_filiale:
    window = Toplevel(root)
    sediu.adauga_filiala(window)


else:
    filiala = ttk.Combobox(root, value=lista_filiale)
    filiala.current(0)
    filiala.pack()

root.mainloop()