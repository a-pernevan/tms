try:
    from database.datab import connection, cursor
except:
    print("Error")
    quit()

cursor.execute("SELECT * from tauros_park_main")
results = cursor.fetchall()

print(results)

cursor.close()
connection.close()