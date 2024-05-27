from datetime import datetime, timedelta

# Get the current datetime
current_time = datetime.now()

print(current_time)

# Add 9 hours to the current time
nine_hours_from_now = current_time + timedelta(hours=12)

print(nine_hours_from_now)

print(nine_hours_from_now - current_time)

# Format the result as 'HH:MM:SS'
formatted_time = '{:%Y-%m-%d %H:%M:%S}'.format(nine_hours_from_now)
dbtime = str(formatted_time)
print(dbtime)
dbtime_back = datetime.strptime(dbtime, "%Y-%m-%d %H:%M:%S")

print(type(dbtime_back))
print(f"Date and time from database in new format: {dbtime_back} ")

print(dbtime_back - current_time)

# print(f"Nine hours from now: {formatted_time}")