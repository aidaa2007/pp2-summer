import json

# Python Dictionary
student = {
    "name": "Alina",
    "age": 20,
    "course": "Python"
}



# Convert Python to JSON
json_string = json.dumps(student, indent=4)

print("JSON String:")
print(json_string)

# Parse JSON
parsed = json.loads(json_string)

print("\nParsed JSON:")
print(parsed)

# Write JSON File
with open("student.json", "w") as file:
    json.dump(student, file, indent=4)

print("\nstudent.json created.")

# Read JSON File
with open("student.json", "r") as file:
    data = json.load(file)

print("\nData Read From File:")
print(data)

# Example using sample-data.json
try:
    with open("sample-data.json", "r") as file:
        sample = json.load(file)

    print("\nSample Data:")
    print(sample)

except FileNotFoundError:
    print("\nsample-data.json not found.")