import tkinter as tk

def add_input_field():
    input_field = tk.Entry(frame)
    input_field.pack()
    input_fields.append(input_field)

def save_data():
    print(input_fields)
    for field in input_fields:
        if field.get():
            # Do something with the data
            print("Saved data:", field.get())
        else:
            print("Input field is empty")

root = tk.Tk()
root.title("Dynamic Input Fields")

frame = tk.Frame(root)
frame.pack()

input_fields = []

add_button = tk.Button(root, text="Add Input Field", command=add_input_field)
add_button.pack()

save_button = tk.Button(root, text="Save Data", command=save_data)
save_button.pack()

root.mainloop()