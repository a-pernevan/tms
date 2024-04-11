import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

root = tk.Tk()
root.title("Treeview Demo")
root.geometry("620x200")

columns = ("first_name", "last_name", "email")

tree = ttk.Treeview(root, columns=columns, show="headings")

tree.heading("first_name", text="First Name")
tree.heading("last_name", text="Last Name")
tree.heading("email", text="Email")

contacts = []
for n in range(1, 100):
    contacts.append((f"first {n}", f"last {n}", f"email{n}@example.com"))

for contact in contacts:
    tree.insert("", tk.END, values=contact)


def item_selected(event):
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        record = item["values"]
        showinfo(title="Information", message=", ".join(record))

tree.bind("<<TreeviewSelect>>", item_selected)

scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)

tree.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

root.mainloop()