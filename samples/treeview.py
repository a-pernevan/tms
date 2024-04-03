import tkinter as tk
from tkinter import ttk

class EditableTreeview:
    def __init__(self, root):
        self.root = root
        self.tree = ttk.Treeview(root)
        self.tree.pack()

        # Insert some sample data
        self.tree.insert("", "end", text="Item 1", values=("Value 1", "Value 2"))
        self.tree.insert("", "end", text="Item 2", values=("Value 3", "Value 4"))

        # Bind double-click event to the treeview
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        """Executed when a row is double-clicked."""
        item_id = self.tree.identify_row(event.y)  # Get the clicked row ID
        column = "#0"  # First column (index 0)

        # Get the position of the clicked cell
        x, y, width, height = self.tree.bbox(item_id, column)

        # Calculate the y-axis offset for placing the Entry popup
        pady = height // 2

        # Create an Entry widget (read-only) on top of the clicked cell
        text = self.tree.item(item_id, "text")
        # entry_popup = tk.Entry(self.tree, state="readonly")
        entry_popup = tk.Entry(self.tree)
        entry_popup.insert(0, text)
        entry_popup.place(x=0, y=y + pady, anchor="w", relwidth=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = EditableTreeview(root)
    root.mainloop()