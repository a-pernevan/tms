from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class Registru_parcare:
    def __init__(self, master):
        super().__init__()
        # Cream interfata si notebook-ul
        # self.master = master
        # self.master.title("Registru parcare")
        self.main_window = ttk.Notebook(master, width=900, height=600)
        self.main_window.pack(pady=0)

        self.tauros_frame = Frame(self.main_window)
        self.tauros_frame.pack(fill=BOTH, expand=1, anchor=W)

        self.samsung_frame = Frame(self.main_window)
        self.samsung_frame.pack(fill=BOTH, expand=1, anchor=W)

        self.vizitatori_frame = Frame(self.main_window)
        self.vizitatori_frame.pack(fill=BOTH, expand=1, anchor=W)

        self.main_window.add(self.tauros_frame, text="Tauros")
        self.main_window.add(self.samsung_frame, text="Samsung")
        self.main_window.add(self.vizitatori_frame, text="Vizitatori")

        # self.test_button = Button(self.tauros_frame, text="Test")
        # self.test_button.grid(row=0, column=0)

# Testam aplicatia

if __name__ == "__main__":
    root = Tk()
    root.title("Registru parcare")
    registru = Registru_parcare(root)
    root.mainloop()



        

