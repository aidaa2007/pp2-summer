# Read entire file

with open("sample.txt", "r") as file:
    print(file.read())

# Read line by line

with open("sample.txt", "r") as file:
    print(file.readline())

# Read all lines

with open("sample.txt", "r") as file:
    lines = file.readlines()

print(lines)