import tkinter as tk
from tkinter import ttk

def create_tab(notebook, tab_name):
    # create a frame for the tab
    frame = tk.Frame(notebook)
    label = tk.Label(frame, text=tab_name)
    label.pack()

    # create a button to close the tab
    close_button = tk.Button(frame, text="Close", command=lambda: notebook.forget(notebook.index(frame)))
    close_button.pack()

    # add the frame to the notebook
    notebook.add(frame, text=tab_name)

    return frame

root = tk.Tk()
notebook = tk.ttk.Notebook(root)
tab1 = create_tab(notebook, "Tab 1")
tab2 = create_tab(notebook, "Tab 2")
notebook.pack(expand=True, fill="both")

root.mainloop()