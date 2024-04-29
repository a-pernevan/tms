import tkinter as tk

def search(event):
    query = entry.get()
    if query:
        # Perform search based on the query and update the listbox
        filtered_results = [result for result in results if query.lower() in result.lower()]
        listbox.delete(0, tk.END)
        for result in filtered_results:
            listbox.insert(tk.END, result)
    else:
        listbox.delete(0, tk.END)

results = ["Result 1", "Result 2", "Result 3", "Result 4", "Result 5"]

root = tk.Tk()

entry = tk.Entry(root)
entry.bind("<KeyRelease>", search)  # Bind the KeyRelease event to the search function
entry.pack()

listbox = tk.Listbox(root)
listbox.pack()

root.mainloop()