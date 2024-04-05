import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import webbrowser

load_dotenv()

# def insert_pdf(connection, id, name, pdf_data):
#     try:
#         cursor = connection.cursor()
#         query = "INSERT INTO PROFILE VALUES (%s, %s, %s)"
#         args = (id, name, pdf_data)
#         cursor.execute(query, args)
#         connection.commit()
#         print("PDF inserted successfully!")
#     except Error as e:
#         print(f"Error: {e}")
#     finally:
#         cursor.close()

# # Example usage:
# connection = mysql.connector.connect(
# host = os.getenv("HOST"),
#         user = os.getenv("USER"),
#         passwd = os.getenv("PASS"),
#         database = "blob_test",
#         auth_plugin='mysql_native_password'
# )

# # Read the PDF file as binary data
# with open("samples/test.pdf", "rb") as pdf_file:
#     pdf_data = pdf_file.read()

# insert_pdf(connection, 1, "Employee1", pdf_data)
# connection.close()

if os.path.exists("retrieved.pdf"):
    os.remove("retrieved.pdf")

def retrieve_pdf(connection, id):
    try:
        cursor = connection.cursor()
        query = "SELECT picture FROM PROFILE WHERE id = %s"
        cursor.execute(query, (id,))
        pdf_data = cursor.fetchone()[0]
        return pdf_data
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

# Example usage:
connection = mysql.connector.connect(
    host = os.getenv("HOST"),
    user = os.getenv("USER"),
    passwd = os.getenv("PASS"),
    database = "blob_test",
    auth_plugin='mysql_native_password'
)

retrieved_pdf_data = retrieve_pdf(connection, 1)

# Save the retrieved PDF data to a file
with open("retrieved.pdf", "wb") as output_pdf:
    output_pdf.write(retrieved_pdf_data)

webbrowser.open("retrieved.pdf")



connection.close()