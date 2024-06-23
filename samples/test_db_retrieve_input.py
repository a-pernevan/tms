import tkinter as tk
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def query_database(event=None):
    query = entry.get()
    try:
        cnx = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            passwd=os.getenv("PASS"),
            database=os.getenv("DB"),
            auth_plugin='mysql_native_password'
        )
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM registru WHERE cap_tractor LIKE '%{}%'".format(query))
        results = cursor.fetchall()
        display_results(results)
    except mysql.connector.Error as err:
        print("Error querying database: {}".format(err))
    finally:
        cursor.close()
        cnx.close()

def display_results(results):
    result_listbox.delete(0, tk.END)
    for row in results:
        result_listbox.insert(tk.END, str(row[0]) + "-" + row[1])

def select_result(event):
    selection = result_listbox.curselection()
    if selection:
        result = result_listbox.get(selection[0]).split("-")[1]
        id = result_listbox.get(selection[0]).split("-")[0]
        entry.delete(0, tk.END)
        entry.insert(0, result)

        try:
            cnx = mysql.connector.connect(
                host=os.getenv("HOST"),
                user=os.getenv("USER"),
                passwd=os.getenv("PASS"),
                database=os.getenv("DB"),
                auth_plugin='mysql_native_password'
            )
            cursor = cnx.cursor()
            cursor.execute("SELECT * FROM registru WHERE id LIKE '%{}%'".format(id))
            results = cursor.fetchall()
            
        except mysql.connector.Error as err:
            print("Error querying database: {}".format(err))
        finally:
            cursor.close()
            cnx.close()

        data.delete(0, tk.END)
        data.insert(0, results[0][3])
        time.delete(0, tk.END)
        time.insert(0, results[0][4])

root = tk.Tk()
root.title("Database Query")

entry = tk.Entry(root)
entry.pack()

entry.bind("<KeyRelease>", query_database)

result_listbox = tk.Listbox(root)
result_listbox.pack()
result_listbox.bind("<ButtonRelease-1>", select_result)
result_listbox.bind("<Return>", select_result)

data = tk.Entry(root)
data.pack()

time = tk.Entry(root)
time.pack()

label = tk.Label(root)
label.pack()

root.mainloop()