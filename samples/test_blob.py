import mysql.connector
import os
from dotenv import load_dotenv
import base64
import io
from PIL import Image

load_dotenv()

# Create connection to database
try:
    tms_db = mysql.connector.connect(
        host = os.getenv("HOST"),
        user = os.getenv("USER"),
        passwd = os.getenv("PASS"),
        database = "blob_test",
        auth_plugin='mysql_native_password'
    )
except:
    print("Could not connect to MySQL")
    mysql_error = messagebox.showerror(title="Connection error", message="Could not connect to DB Server")
    quit()
my_cursor = tms_db.cursor()

# # Open a file in binary mode
# file = open('b425edi_talon.png','rb').read()
 
# # We must encode the file to get base64 string
# file = base64.b64encode(file)
 
# # Sample data to be inserted
# args = ('100', 'Talon B425EDI', file)
 
# # Prepare a query
# query = 'INSERT INTO PROFILE VALUES(%s, %s, %s)'
 
# # Execute the query and commit the database.
# my_cursor.execute(query,args)
# tms_db.commit()

# Prepare the query
query = 'SELECT PICTURE FROM PROFILE WHERE ID=100'
 
# Execute the query to get the file
my_cursor.execute(query)
 
data = my_cursor.fetchall()
 
# The returned data will be a list of list
image = data[0][0]
 
# Decode the string
binary_data = base64.b64decode(image)
 
# Convert the bytes into a PIL image
image = Image.open(io.BytesIO(binary_data))
 
# Display the image
image.show()