import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully");

# conn.execute('CREATE TABLE IF NOT EXISTS USERS(fname TEXT, lname TEXT)')
conn.execute("drop table users")
print ("Table created successfully");
conn.close()