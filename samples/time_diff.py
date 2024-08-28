from datetime import datetime

from database.datab import connection, cursor


connection._open_connection()

cursor.execute("SELECT date_in_real, date_in_out from tauros_park_main WHERE place_id = 50")

result = cursor.fetchall()

connection.close()

print(str(result[0][0]))

# date_in = datetime.strptime(str(result[0][0]), "%Y %m %d %H %M %S")

# print(date_in)

# Create datetime objects
# datetime1 = datetime(result[0][0])  # August 28, 2024, 14:30 (2:30 PM)
# datetime2 = datetime(2024, 8, 29, 18, 45)  # August 29, 2024, 18:45 (6:45 PM)

# Calculate the difference between two datetime objects
time_difference = result[0][1] - result[0][0]

# Get the total number of hours
hours_difference = time_difference.total_seconds() / 3600

hours_difference = round(hours_difference, 0)

print(f"Difference in hours: {hours_difference} hours")
