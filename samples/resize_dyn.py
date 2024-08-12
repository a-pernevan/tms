import tkinter as tk

root = tk.Tk()
root.title("Dynamic Resize")

frame = tk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

label = tk.Label(frame, text="Dynamic Resize")
label.grid(row=0, column=0, sticky="ew")

button = tk.Button(frame, text="Button")
button.grid(row=1, column=0, sticky="ew")

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

root.mainloop()