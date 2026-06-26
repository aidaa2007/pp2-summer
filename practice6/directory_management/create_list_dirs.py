import os

# Create directories

os.makedirs("test_folder/subfolder", exist_ok=True)

print("Directories created.")

# Current directory

print("Current directory:")
print(os.getcwd())

# List files and folders

print("Contents:")
print(os.listdir())