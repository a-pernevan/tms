import tkinter as tk

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Centered Widgets Example")

        # Create the content frame
        self.contentFrame = tk.Frame(self.root)
        self.contentFrame.grid(row=0, column=0)

        # Create the topBar frame (centered horizontally)
        self.topBar = tk.Frame(self.contentFrame, border=2, relief=tk.RAISED)
        self.topBar.grid(row=0, column=0, columnspan=23)

        # Create the New Game button (centered within topBar)
        self.newGameButton = tk.Button(self.topBar, text="New Game")
        self.newGameButton.grid(row=0, column=0)

        # Create the message label (centered within topBar)
        self.messageBox = tk.Label(self.topBar, text="Hello, World!", height=2)
        self.messageBox.grid(row=1, column=0, sticky=tk.W + tk.E)

        # Set weights for rows and columns to allow expansion
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.contentFrame.grid_columnconfigure(0, weight=1)
        self.contentFrame.grid_rowconfigure(0, weight=1)
        self.topBar.grid_columnconfigure(0, weight=1)
        self.topBar.grid_rowconfigure(0, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
