import tkinter as tk
from tkinter import ttk 
from tkcalendar import Calendar, DateEntry

window = tk.Tk()
cal = DateEntry(window)
date = cal.datetime.today() + cal.timedelta(days=2)
cal.calevent_create(date, 'Hello World', 'message')
cal.tag_config('message', background='red', foreground='yellow')
cal.pack()

window.mainloop()