# import add_client
from tkinter import *
from tkinter import ttk
from classes.clients import Clients

root = Tk()
root.title("TMS Project")
root.geometry("900x600")

main_window = ttk.Notebook(root)
main_window.pack(pady=0)

main_frame = Frame(main_window, width=800, height=500)
client_frame = Frame(main_window, width=800, height=500)

main_frame.pack(fill=BOTH, expand=1)
client_frame.pack(fill=BOTH, expand=1)

main_window.add(main_frame, text="Principal")
main_window.add(client_frame, text="Gestionare clienti")

hello = Clients(main_frame)



# add_client

root.mainloop()