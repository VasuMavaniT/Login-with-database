import psycopg2
import random

# Initialize counters for each role
role_counters = {
    'admin': 1,
    'developer': 1,
    'user': 1
}

# Function to generate random username, password, and role
def generate_random_data():
    roles = ['admin', 'developer', 'user']  # List of roles
    role = random.choice(roles)  # Randomly select a role
    num = role_counters[role]  # Get the current counter value for the selected role
    
    username = f"{role}{num}"
    password = username  # Making password same as username for simplicity
    
    role_counters[role] += 1  # Increment the counter for the selected role
    
    return username, password, role

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

# Insert 100 random records into the table
for i in range(100):
    username, password, role = generate_random_data()
    cur.execute("INSERT INTO UsersData (username, password, role) VALUES (%s, %s, %s);", (username, password, role))

# Close cursor and connection
cur.close()
conn.close()

print("Table 'Users' updated successfully with 100 random records inserted.")
