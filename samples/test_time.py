from datetime import datetime, timedelta

# Get the current datetime
current_time = datetime.now()

print(current_time)

# Add 9 hours to the current time
nine_hours_from_now = current_time + timedelta(hours=12)

print(nine_hours_from_now)

print(nine_hours_from_now - current_time)

# Format the result as 'HH:MM:SS'
# formatted_time = '{:%Y-%m-%d %H:%M:%S}'.format(nine_hours_from_now)

# print(f"Nine hours from now: {formatted_time}")