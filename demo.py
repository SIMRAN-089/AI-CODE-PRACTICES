import os

file_path = "mail_data.csv"
print("Looking for file in:", os.getcwd())

if os.path.exists(file_path):
    print("✅ File found!")
else:
    print("❌ File not found! Move 'mail_data.csv' to:", os.getcwd())
