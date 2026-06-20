from datetime import datetime, timedelta, timezone

# Current Date and Time
now = datetime.now()
print("Current Date and Time:")
print(now)





# Create Specific Date
birthday = datetime(2005, 8, 15)
print("\nBirthday:")
print(birthday)




# Date Formatting
print("\nFormatted Date:")
print(now.strftime("%Y-%m-%d %H:%M:%S"))




# Time Difference
future = now + timedelta(days=30)

difference = future - now

print("\nDays Until Future Date:")
print(difference.days)




# Timezone Example
utc_time = datetime.now(timezone.utc)

print("\nUTC Time:")
print(utc_time)



# Another timezone (+6 UTC Kazakhstan example)
kz_timezone = timezone(timedelta(hours=6))
kz_time = datetime.now(kz_timezone)

print("\nKazakhstan Time:")
print(kz_time)