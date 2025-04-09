import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Fetch all users
cursor.execute("SELECT * FROM user")
users = cursor.fetchall()

# Print results
for user in users:
    print(user)

conn.close()
