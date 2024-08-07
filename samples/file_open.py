import tempfile
import subprocess
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Button, filedialog, messagebox
try:
    from database.datab import connection, cursor
except:
    mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server, program will exit")
    quit()
import os
import webbrowser
from classes.tooltip import ToolTip


def save_pdf(pdf_path):
    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if save_path:
        try:
            with open(pdf_path, 'rb') as src_file:
                pdf_data = src_file.read()
            with open(save_path, 'wb') as dest_file:
                dest_file.write(pdf_data)
            messagebox.showinfo("Success", f"PDF saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF: {e}")

    # Delete the temporary file
    os.remove(pdf_path)
    print(f"Temporary file {pdf_path} deleted.")

def delete_pdf():
    connection._open_connection()
    sql = "DELETE FROM documente_remorci WHERE id_tms = '35' AND numar_auto = 'AR15UUT' AND tip_doc = 'CIV'"
    cursor.execute(sql)
    connection.commit()
    connection.close()
    root.withdraw()
    messagebox.showinfo(title="Success", message="PDF deleted successfully!")
    root.deiconify()

def load_pdf(pdf_path):
    # print(pdf_data)
    # try:
    #     if os.name == 'nt':  # For Windows
    #         subprocess.run(['start', pdf_path], shell=True)
    #     elif os.name == 'posix':  # For Unix-like (macOS, Linux)
    #         subprocess.run(['open', pdf_path] if sys.platform == 'darwin' else ['xdg-open', pdf_path])
    # except Exception as e:
    #     print(f"Failed to open PDF: {e}")
    #     return

    try:
        if os.name == 'nt':  # For Windows
            process = subprocess.Popen(['start', pdf_path], shell=True)
            process.communicate()  # Waits for the process to complete
        elif sys.platform == 'darwin':  # For macOS
            process = subprocess.run(['open', pdf_path])
        else:  # For Unix-like (Linux)
            process = subprocess.run(['xdg-open', pdf_path])
    except Exception as e:
        print(f"Failed to open PDF: {e}")
        return


    # Wait for the user to close the viewer
    messagebox.showinfo(title="Success", message="PDF opened successfully! Press ok to delete temp file")

    # Delete the temporary file
    os.remove(pdf_path)
    print(f"Temporary file {pdf_path} deleted.")

def check_pdf():
    try:
        connection._open_connection()
        cursor.execute("SELECT doc FROM documente_remorci WHERE id_tms = '35' AND numar_auto = 'AR15UUT' AND tip_doc = 'CIV'")
        pdf_data = cursor.fetchone()[0]
        temp_pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_pdf_file.write(pdf_data)
        temp_pdf_path = temp_pdf_file.name
        temp_pdf_file.close()
        return temp_pdf_path

    except:
        print(f"Error!")
        return None
    
    finally:
        connection.close()

def insert_pdf(pdf_data):
    try:
        connection._open_connection()
        print("Connection ok")
        sql = "INSERT INTO documente_remorci (id_tms, numar_auto, tip_doc, doc) VALUES (%s, %s, %s, %s)"
        values = ("35", "AR15UUT", "CIV", pdf_data)
        cursor.execute(sql, values)
        connection.commit()
        messagebox.showinfo(title="Success", message="PDF inserted successfully!")

    except :
        print(f"Error!")
    finally:
        connection.close()

def open_file_dialog():
    # Open file dialog and store the selected file path
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("Text files", "*.pdf"), ("All files", "*.*"))
    )
    # If a file is selected, print its path
    if file_path:
        print(f"Selected file: {file_path}")
        with open(file_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
            # webbrowser.open(pdf_data)
            insert_pdf(pdf_data)

# Create the main application window
root = tk.Tk()
root.title("File Upload Example")
root.geometry("400x300")

# Cream icoanele pentru butoane
icon_open = Image.open("samples/icons/open-icon-11.jpg")
icon_open = icon_open.resize((33, 33))
icon_open = ImageTk.PhotoImage(icon_open)

icon_delete = Image.open("samples/icons/icon-delete-19.jpg")
icon_delete = icon_delete.resize((33, 33))
icon_delete = ImageTk.PhotoImage(icon_delete)

icon_upload = Image.open("samples/icons/upload-icon-22.jpg")
icon_upload = icon_upload.resize((33, 33))
icon_upload = ImageTk.PhotoImage(icon_upload)

icon_save = Image.open("samples/icons/save-image-icon-11.jpg")
icon_save = icon_save.resize((33, 33))
icon_save = ImageTk.PhotoImage(icon_save)

# Create a label to display the selected file path
file_label = tk.Label(root, text="CIV remorca AR15UUT")
file_label.pack(pady=20)


# Create a button to open the file dialog
open_button = tk.Button(root, text="Open File", image=icon_upload, borderwidth=0, highlightthickness=0, relief="flat", command=open_file_dialog)
open_button.pack(pady=20)
ToolTip(open_button, text="Upload file")

if check_pdf():
    # Modificam butonul sa apara ca o poza
    open_button.config(state="disabled")
    open_button.pack_forget()
    file_label.config(text="CIV remorca AR15UUT already uploaded")
    load_button = Button(root, image=icon_open, text="Load file", borderwidth=0, highlightthickness=0, relief="flat", command=lambda : load_pdf(check_pdf()))
    load_button.pack(pady=20)

    # Adaugam text on hover
    ToolTip(load_button, text="Open file")

    save_button = Button(root, text="Save file", image=icon_save, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: save_pdf(check_pdf()))
    save_button.pack(pady=20)
    ToolTip(save_button, text="Save file")

    delete_button = Button(root, text="Delete file", image=icon_delete, borderwidth=0, highlightthickness=0, relief="flat", command=delete_pdf)
    delete_button.pack(pady=20)
    ToolTip(delete_button, text="Delete file")

else:
    file_label.config(text="CIV remorca AR15UUT not uploaded")


# Start the Tkinter event loop
root.mainloop()
