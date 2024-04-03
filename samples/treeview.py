from tkinter import *
from tkinter import ttk


root = Tk()
root.title("TKinter Treeview")
root.geometry("500x750")

# add some style
style = ttk.Style()
# Pick a theme
style.theme_use("default")
# configure treeview colors

style.configure("Treeview",
                background = "#D3D3D3",
                foreground = "black",
                rowheight = 25,
                fieldbackground = "#D3D3D3"                
                )

# Change selected color
style.map("Treeview", 
          background=[("selected", "green")])

# Create Treeview frame
tree_frame = Frame(root)
tree_frame.pack(pady=20)

# Treeview scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")

# Configure scrollbar
tree_scroll.config(command=my_tree.yview)

# Define our columns
my_tree["columns"] = ("Name", "ID", "Favorite Pizza")

# format our columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Name", anchor=W, width=140)
my_tree.column("ID", anchor=CENTER, width=100)
my_tree.column("Favorite Pizza", anchor=W, width=140)

# Create headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("Favorite Pizza", text="Favorite Pizza", anchor=W)

# Add data
data = [
    ["Andrei", 1, "Tonno"],
    ["Vali", 2, "Quattro Fromagi"],
    ["Alex", 3, "Chicken"],
    ["Radu", 4, "Hot"],
    ["Moro", 5, "Corn"],
    ["Andrei", 1, "Tonno"],
    ["Vali", 2, "Quattro Fromagi"],
    ["Alex", 3, "Chicken"],
    ["Radu", 4, "Hot"],
    ["Moro", 5, "Corn"],
    ["Andrei", 1, "Tonno"],
    ["Vali", 2, "Quattro Fromagi"],
    ["Alex", 3, "Chicken"],
    ["Radu", 4, "Hot"],
    ["Moro", 5, "Corn"],
    ["Andrei", 1, "Tonno"],
    ["Vali", 2, "Quattro Fromagi"],
    ["Alex", 3, "Chicken"],
    ["Radu", 4, "Hot"],
    ["Moro", 5, "Corn"]
]

# Create striped row tags
my_tree.tag_configure("oddrow", background="white")
my_tree.tag_configure("evenrow", background="lightblue")

global count
count = 0
for record in data:
    if count % 2 == 0:
        my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]), tags=('evenrow',))
    else:
        my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]), tags=('oddrow',))
    count += 1


'''
my_tree.insert(parent='', index='end', iid=0, text="", values=("John", 1, "Pepperoni"))
my_tree.insert(parent='', index='end', iid=1, text="", values=("Andrei", 2, "Tonno"))
my_tree.insert(parent='', index='end', iid=2, text="", values=("Vali", 3, "Quattro Fromagi"))
my_tree.insert(parent='', index='end', iid=3, text="", values=("Alex", 4, "Chicken"))
'''

# Add child
# my_tree.insert(parent='1', index='end', iid=4, text="Child", values=("Alex", 2.2, "Chicken"))
# my_tree.move('4', '1', '1')

my_tree.pack()

add_frame = Frame(root)
add_frame.pack(pady=20)

# Labels
nl = Label(add_frame, text="Name")
nl.grid(row=0, column=0)

il = Label(add_frame, text="ID")
il.grid(row=0, column=1)

tl = Label(add_frame, text="Topping")
tl.grid(row=0, column=2)

# Entry boxes
name_box = Entry(add_frame)
name_box.grid(row=1, column=0)

id_box = Entry(add_frame)
# id_box.insert(0, count+1)
id_box.grid(row=1, column=1)

topping_box = Entry(add_frame)
topping_box.grid(row=1, column=2)

# Add record function
def add_record():
    global count
    if count % 2 == 0:
        my_tree.insert(parent='', index='end', iid=count, text="", values=(name_box.get(), id_box.get(), topping_box.get()), tags=("evenrow",))
    else:
        my_tree.insert(parent='', index='end', iid=count, text="", values=(name_box.get(), id_box.get(), topping_box.get()), tags=("oddrow",))
    
    count += 1

    # Clear the boxes
    name_box.delete(0, END)
    id_box.delete(0, END)
    topping_box.delete(0, END)
    # id_box.insert(0, count+1)

def remove_all():
    for record in my_tree.get_children():
        my_tree.delete(record)


# Remove one selected
def remove_one():
    x = my_tree.selection()[0]
    my_tree.delete(x)


# Remove many selected
def remove_many():
    x = my_tree.selection()
    for record in x:
        # print(record)
        my_tree.delete(record)

    
# Select record
def select_record():
    # Clear entry boxes
    name_box.delete(0, END)
    id_box.delete(0, END)
    topping_box.delete(0, END)

    # Grab record number
    selected = my_tree.focus()
    # Grab record values
    values = my_tree.item(selected, "values")
    # temp_label.config(text=values[0])

    # Output to entry boxes
    name_box.insert(0, values[0])
    id_box.insert(0, values[1])
    topping_box.insert(0, values[2])

# Save updated record
def update_record():
    # Grab record number
    selected = my_tree.focus()
    # Save new data
    my_tree.item(selected, text="", values=(name_box.get(), id_box.get(), topping_box.get()))
    # Clear entry boxes
    name_box.delete(0, END)
    id_box.delete(0, END)
    topping_box.delete(0, END)

# Move row up
def up():
    rows = my_tree.selection()
    for row in rows:
        my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)

# Move row down
def down():
    rows = my_tree.selection()
    for row in reversed(rows):
        my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)

# Create binding click function
def clicker(e):
    select_record()

# buttons
move_up = Button(root, text="Move Up", command = up)
move_up.pack(pady=5)

move_down = Button(root, text="Move Down", command = down)
move_down.pack(pady=5)

select_button = Button(root, text="Select record", command=select_record)
select_button.pack(pady=5)

update_button = Button(root, text="Update record", command=update_record)
update_button.pack(pady=5)

add_record = Button(root, text="Add Record", command=add_record)
add_record.pack(pady=5)

# Remove all
remove_all = Button(root, text="Remove all records", command = remove_all)
remove_all.pack(pady=5)

# Remove one
remove_one = Button(root, text="Remove one selected", command = remove_one)
remove_one.pack(pady=5)

# Remove many selected
remove_many = Button(root, text="Remove many selected", command = remove_many)
remove_many.pack(pady=5)

temp_label = Label(root, text="")
temp_label.pack(pady=20)

# Bindings
# my_tree.bind("<Double-1>", clicker)
my_tree.bind("<ButtonRelease-1>", clicker)
root.mainloop()