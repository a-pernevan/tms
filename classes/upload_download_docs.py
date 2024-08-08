import tempfile
import sys
import subprocess
import tkinter as tk
from tkinter import Toplevel, ttk
from PIL import Image, ImageTk
from tkinter import W, Button, filedialog, messagebox
try:
    from database.datab import connection, cursor
except:
    mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server, program will exit")
    quit()
import os
import webbrowser
from utils.tooltip import ToolTip
from liste import Documente_remorci

class Documente:
    def __init__(self, master, id_tms, numar_auto):
        self.master = master
        self.id_tms = id_tms
        self.numar_auto = numar_auto
        self.interfata()

    def interfata(self):
        # Cream icoanele pentru butoane
        self.icon_open = Image.open("classes/utils/icons/open-icon-11.jpg")
        self.icon_open = self.icon_open.resize((22, 22))
        self.icon_open = ImageTk.PhotoImage(self.icon_open)

        self.icon_delete = Image.open("classes/utils/icons/icon-delete-19.jpg")
        self.icon_delete = self.icon_delete.resize((22, 22))
        self.icon_delete = ImageTk.PhotoImage(self.icon_delete)

        self.icon_upload = Image.open("classes/utils/icons/upload-icon-22.jpg")
        self.icon_upload = self.icon_upload.resize((22, 22))
        self.icon_upload = ImageTk.PhotoImage(self.icon_upload)

        self.icon_save = Image.open("classes/utils/icons/save-image-icon-11.jpg")
        self.icon_save = self.icon_save.resize((22, 22))
        self.icon_save = ImageTk.PhotoImage(self.icon_save)

        self.icon_new = Image.open("classes/utils/icons/add-text-icon-15.jpg")
        self.icon_new = self.icon_new.resize((22, 22))
        self.icon_new = ImageTk.PhotoImage(self.icon_new)


        self.frame_docs = tk.LabelFrame(self.master, text="Documente:")
        self.frame_docs.pack(padx=5, pady=5)

        # self.doc_existente_ = tk.LabelFrame(self.frame_docs, text="Documente incarcate:")
        # self.doc_existente_label.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.adauga_doc_label = tk.Label(self.frame_docs, text="Adauga document:")
        self.adauga_doc_label.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.add_new_button = tk.Button(self.frame_docs, image=self.icon_new, borderwidth=0, highlightthickness=0, relief="flat", command=self.incarca_document_nou)
        self.add_new_button.grid(row=0, column=1, sticky=W, padx=10, pady=10)
        ToolTip(self.add_new_button, text="Adauga document")

        lista_documente = self.verifica_doc_existente()
        print(lista_documente)
        if len(lista_documente) > 0:
            for i, doc in enumerate(lista_documente):

                b = 0
                # print(1, doc[0])
                tk.Label(self.frame_docs, text=doc[0]).grid(row=i+1, column=b, sticky=W, padx=10, pady=10)
                self.open_button = tk.Button(self.frame_docs, image=self.icon_open, borderwidth=0, highlightthickness=0, relief="flat", command=lambda doc=doc[0]: self.deschide_document(doc))
                self.open_button.grid(row=i+1, column=b+1, sticky=W, padx=10, pady=10)
                ToolTip(self.open_button, text="Deschide documentul")

                self.save_button = tk.Button(self.frame_docs, image=self.icon_save, borderwidth=0, highlightthickness=0, relief="flat", command=lambda doc=doc[0]: self.salveaza_document(doc))
                self.save_button.grid(row=i+1, column=b+2, sticky=W, padx=10, pady=10)
                ToolTip(self.save_button, text="Salveaza documentul")

                self.delete_button = tk.Button(self.frame_docs, image=self.icon_delete, borderwidth=0, highlightthickness=0, relief="flat", command=lambda doc=doc[0]: self.sterge_document(doc))
                self.delete_button.grid(row=i+1, column=b+3, sticky=W, padx=10, pady=10)
                ToolTip(self.delete_button, text="Sterge documentul")
                


                # self.lipsa_documente(i+2, 0, i+3)

        else: 
            # tk.Label(self.frame_docs, text="Nu exista documente incarcate.").grid(row=0, column=0, sticky=W, padx=10, pady=10)
            # self.adauga_doc_label = tk.Label(self.frame_docs, text="Adauga document:")
            # self.adauga_doc_label.grid(row=1, column=0, sticky=W, padx=10, pady=10)
            # self.lista_documente = Documente_remorci.afisare_documente(self.master)
            # self.tip_doc = tk.StringVar()
            # self.lista_documente_drop = ttk.Combobox(self.frame_docs, textvariable=self.tip_doc, values=self.lista_documente)
            # self.lista_documente_drop.grid(row=1, column=1, sticky=W, padx=10, pady=10)
            # self.upload_button = tk.Button(self.frame_docs, image=self.icon_upload, borderwidth=0, highlightthickness=0, relief="flat", command=self.selecteaza_document)
            # self.upload_button.grid(row=1, column=2, sticky=W, padx=10, pady=10)
            # ToolTip(self.upload_button, text="Incarca document")
            tk.Label(self.frame_docs, text="Nu exista documente incarcate.").grid(row=1, column=0, sticky=W, padx=10, pady=10)
            # self.add_new_button = tk.Button(self.frame_docs, image=self.icon_new, borderwidth=0, highlightthickness=0, relief="flat", command=self.incarca_document_nou)
            # self.add_new_button.grid(row=0, column=1, sticky=W, padx=10, pady=10)
            # ToolTip(self.add_new_button, text="Adauga document")

        # self.adauga_doc_frame = tk.Frame(self.frame_docs)
        # self.adauga_doc_frame.grid()


    def verifica_doc_existente(self):
        documente_incarcate = []
        connection._open_connection()
        sql = "SELECT tip_doc FROM documente_remorci WHERE id_tms = %s AND numar_auto = %s"
        values = (self.id_tms, self.numar_auto)
        cursor.execute(sql, values)
        result = cursor.fetchall()
        connection.close()
        if result:
            for doc in result:
                documente_incarcate.append(doc)
            return documente_incarcate

        else:
            return []
        
    def descarca_document(self, tip_doc):
        connection._open_connection()
        sql = "SELECT doc FROM documente_remorci WHERE id_tms = %s AND numar_auto = %s AND tip_doc = %s"
        values = (self.id_tms, self.numar_auto, tip_doc)
        cursor.execute(sql, values)
        pdf_data = cursor.fetchone()[0]
        connection.close()
        if pdf_data:
            temp_pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_pdf_file.write(pdf_data)
            temp_pdf_path = temp_pdf_file.name
            temp_pdf_file.close()
            return temp_pdf_path
        else:
            return None
        
    def deschide_document(self, doc):
        pdf_path = self.descarca_document(doc)
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

    def salveaza_document(self, doc):
        pdf_path = self.descarca_document(doc)

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

    def sterge_document(self, doc):
        connection._open_connection()
        sql = "DELETE FROM documente_remorci WHERE id_tms = %s AND numar_auto = %s AND tip_doc = %s"
        values = (self.id_tms, self.numar_auto, doc)
        cursor.execute(sql, values)
        connection.commit()
        connection.close()
        # root.withdraw()
        messagebox.showinfo(title="Success", message="PDF deleted successfully!")
        # root.deiconify()
        self.frame_docs.pack_forget()
        self.interfata()

    def selecteaza_document(self):
        doc = self.lista_documente_drop.get()
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
                self.incarca_document(doc, pdf_data)

    def incarca_document(self, doc, pdf_data):
        
        try:
            connection._open_connection()
            print("Connection ok")
            sql = "INSERT INTO documente_remorci (id_tms, numar_auto, tip_doc, doc) VALUES (%s, %s, %s, %s)"
            values = (self.id_tms, self.numar_auto, doc, pdf_data)
            cursor.execute(sql, values)
            connection.commit()
            self.ok_message_doc_load = messagebox.showinfo(title="Success", message="PDF inserted successfully!")
            if self.ok_message_doc_load == "ok":
                self.fereastra.destroy()

        except :
            messagebox.showerror(title="Error", message="Failed to insert PDF!")
        finally:
            connection.close()
            self.frame_docs.pack_forget()
            self.document_nou_frame.pack_forget()
            self.interfata()

    def lipsa_documente(self, row, column, frame):
            
            def actualizeaza_lista_docs(e):
                doc_window = Toplevel(self.master)
                doc_window.transient(self.master)
                doc_window.grab_set()
                get_docs = Documente_remorci(self.master)
                get_docs.adauga_tip_doc(doc_window)
                doc_window.wait_window()
                lista_documente = get_docs.afisare_doc()
                self.lista_documente_drop.configure(values=lista_documente)

            self.document_nou_frame = tk.Frame(frame)
            self.document_nou_frame.grid(row=row, column=column, sticky=W)
            self.adauga_doc_label = tk.Label(self.document_nou_frame, text="Adauga document:")
            self.adauga_doc_label.grid(row=1, column=0, sticky=W, padx=10, pady=10)
            self.remorca_docs = Documente_remorci(self.master)
            self.lista_documente = self.remorca_docs.afisare_doc()
            self.tip_doc = tk.StringVar()
            self.lista_documente_drop = ttk.Combobox(self.document_nou_frame, textvariable=self.tip_doc, values=self.lista_documente)
            self.lista_documente_drop.grid(row=1, column=1, sticky=W, padx=10, pady=10)
            self.lista_documente_drop.bind("<Double-1>", actualizeaza_lista_docs)
            self.upload_button = tk.Button(self.document_nou_frame, image=self.icon_upload, borderwidth=0, highlightthickness=0, relief="flat", command=self.selecteaza_document)
            self.upload_button.grid(row=1, column=2, sticky=W, padx=10, pady=10)
            ToolTip(self.upload_button, text="Incarca document")
            


    def incarca_document_nou(self):
        self.fereastra = tk.Toplevel(self.master)
        self.fereastra.transient(self.master)
        self.fereastra.grab_set()
        self.fereastra.title("Incarca document")
        # fereastra.geometry("300x300")

        self.lipsa_documente(0, 0, self.fereastra)

        self.fereastra.wait_window()

        # self.fereastra.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    obj = Documente(root, 35, 'AR15UUT')
    # obj.interfata()
    root.mainloop()