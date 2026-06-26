import shutil
import os

os.makedirs("backup", exist_ok=True)

if os.path.exists("sample.txt"):
    shutil.copy("sample.txt", "backup/sample.txt")
    print("File copied to backup folder.")
else:
    print("sample.txt not found.")