from tkinter import *
from tkinter import messagebox

class Clients:
    def __init__(self, root):
        my_frame = LabelFrame(root, text="Test class", padx=10, pady=10)
        my_frame.pack()
        button_test = Button(root, text="Test", command=self.button_test)
        button_test.pack()

    def button_test(self):
        self.message = messagebox.showinfo(title="Test", message="This is a test")
        