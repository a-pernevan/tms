from database.datab import connection, cursor

cursor.execute("SELECT * from tauros_park_main")
results = cursor.fetchall()

print(results)

cursor.close()
connection.close()