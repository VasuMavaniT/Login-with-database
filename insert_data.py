import psycopg2
import random
import bcrypt

def hash_password(password):
    """Hash a password for storing."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def generate_random_data(role_counters):
    roles = ['admin', 'developer', 'user']  # List of roles
    role = random.choice(roles)  # Randomly select a role
    num = role_counters[role]  # Get the current counter value for the selected role
    
    username = f"{role}{num}"
    password = username  # For simplicity, making password same as username
    hashed_password = hash_password(password)  # Hash the password
    role_counters[role] += 1  # Increment the counter for the selected role
    
    return username, hashed_password.decode('utf-8'), role

# Initialize counters for each role
role_counters = {
    'admin': 1,
    'developer': 1,
    'user': 1
}

# Connect to PostgreSQL server
conn = psycopg2.connect(
    dbname="mydatabase",  # Your database name
    user="postgres",      # Default superuser
    password="admin",     # Password for the superuser
    host="localhost"      # Host where PostgreSQL is running
)
conn.autocommit = True
cur = conn.cursor()

# Insert 100 random records into the table
for i in range(100):
    username, hashed_password, role = generate_random_data(role_counters)
    cur.execute("INSERT INTO UsersData (username, password, role) VALUES (%s, %s, %s);", (username, hashed_password, role))

# Close cursor and connection
cur.close()
conn.close()
print("Table 'UsersData' updated successfully with 100 random records inserted.")
