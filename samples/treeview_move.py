import tkinter as tk
from tkinter import ttk

class TreeviewColumnDrag(tk.Frame):
    def __init__(self, parent, treeview):
        super().__init__(parent)
        self.treeview = treeview
        self.column_dragging = None
        self.column_dragging_offset = None
        self.bind('<ButtonPress-1>', self.on_column_press)
        self.bind('<B1-Motion>', self.on_column_move)
        self.bind('<ButtonRelease-1>', self.on_column_release)

    def on_column_press(self, event):
        # Get the column index of the pressed column
        column_index = self.treeview.identify_column(event.x)
        # Check if the pressed column is draggable
        if self.treeview.tag_configure(column_index, 'draggable'):
            self.column_dragging = column_index
            self.column_dragging_offset = event.x - self.treeview.winfo_x()

    def on_column_move(self, event):
        if self.column_dragging:
            # Calculate the new position of the dragged column
            new_x = event.x_root - self.treeview.winfo_rootx() - self.column_dragging_offset
            # Move the column to the new position
            self.treeview.column(self.column_dragging, width=new_x)

    def on_column_release(self, event):
        if self.column_dragging:
            self.column_dragging = None
            self.column_dragging_offset = None

root = tk.Tk()

treeview = ttk.Treeview(root)
treeview.pack()

# Add some columns to the Treeview
treeview['columns'] = ('column1', 'column2', 'column3')
for column in treeview['columns']:
    treeview.heading(column, text=column)
    # Make the columns draggable
    treeview.tag_configure(column, draggable=True)

# Create a TreeviewColumnDrag instance for the Treeview
treeview_column_drag = TreeviewColumnDrag(root, treeview)
treeview_column_drag.pack()

root.mainloop()