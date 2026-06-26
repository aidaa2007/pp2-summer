# Create and write to a file

with open("sample.txt", "w") as file:
    file.write("Hello, Python!\n")
    file.write("This is Practice 6.\n")

print("File created and written successfully.")

# Append data

with open("sample.txt", "a") as file:
    file.write("This line was appended.\n")

print("Data appended.")