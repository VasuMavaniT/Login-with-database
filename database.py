import psycopg2
import random
import string

# Function to generate random username and password
def generate_random_data(num):
    username = "user" + str(num)
    password = "password" + str(num)
    return username, password

# Connect to PostgreSQL server
conn = psycopg2.connect(
    dbname="mydatabase",  # Your database name
    user="postgres",      # Default superuser
    password="admin",     # Password for the superuser
    host="localhost"      # Host where PostgreSQL is running
)

# Set autocommit to True
conn.autocommit = True

# Create a cursor
cur = conn.cursor()

# Insert 10 random records into the table
for i in range(100):
    username, password = generate_random_data(i)
    cur.execute("INSERT INTO Users (username, password) VALUES (%s, %s);", (username, password))

# Close cursor and connection
cur.close()
conn.close()

print("Table 'Users' created successfully with 10 random records inserted.")
