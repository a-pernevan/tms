import tkinter as tk
from tkinter import ttk

def close_frame(event):
    frame = event.widget
    frame.forget()

root = tk.Tk()
root.geometry("400x400")

notebook = ttk.Notebook(root)
notebook.pack()

frame1 = ttk.Frame(notebook)
frame1.pack()

frame2 = ttk.Frame(notebook)
frame2.pack()

notebook.add(frame1, text="Frame 1")
notebook.add(frame2, text="Frame 2")

frame1.bind("<Button-1>", close_frame)
frame2.bind("<Button-1>", close_frame)

root.mainloop()