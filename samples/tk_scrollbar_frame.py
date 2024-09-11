import tkinter as tk

root = tk.Tk()

# Create a canvas and add it to the root window
canvas = tk.Canvas(root, width=400, height=200)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Create a scrollbar and add it to the root window
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas to use the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=canvas.yview)

# Create a frame and add it to the canvas
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor='nw')

# Add some widgets to the frame to test the scrollbar
for i in range(20):
    tk.Label(frame, text=f"Label {i}").pack()

# Update the canvas to show the scrollbar
frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

root.mainloop()