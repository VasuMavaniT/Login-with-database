import psycopg2
import random
import bcrypt

def hash_password(password):
    """Hash a password for storing."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def connect_db():
    """Establishes a database connection."""
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="postgres",
        password="admin",
        host="localhost"
    )
    conn.autocommit = True
    return conn

def initialize_roles(cur):
    """Initializes roles in the Roles table and returns a mapping of role names to role IDs."""
    roles = [('R1', 'admin'), ('R2', 'developer'), ('R3', 'user')]
    cur.executemany("INSERT INTO Roles (roleid, rolename) VALUES (%s, %s) ON CONFLICT DO NOTHING;", roles)
    return {name: rid for rid, name in roles}

def insert_users_and_roles(cur, role_mapping):
    """Inserts users and their roles into the database."""
    role_counters = {role: 1 for role in role_mapping.values()}  # Initialize counters for each role

    # Insert 100 random records into users and UserRoles tables
    for i in range(100):
        role = random.choice(list(role_mapping.keys()))  # Randomly select a role
        username = f"{role}{role_counters[role_mapping[role]]}"
        userid = f"U{username}"
        password = username  # For simplicity, making password same as username
        hashed_password = hash_password(password)  # Hash the password

        # Insert user
        cur.execute("INSERT INTO users (userid, username, password) VALUES (%s, %s, %s);",
                    (userid, username, hashed_password.decode('utf-8')))

        # Insert user role mapping
        cur.execute("INSERT INTO UserRoles (userid, roleid) VALUES (%s, %s);",
                    (userid, role_mapping[role]))

        # Increment the counter for the selected role
        role_counters[role_mapping[role]] += 1

def insert_data():
    conn = connect_db()
    cur = conn.cursor()

    # Initialize roles and get role mapping
    role_mapping = initialize_roles(cur)

    # Insert users and their roles
    insert_users_and_roles(cur, role_mapping)

    # Close cursor and connection
    cur.close()
    conn.close()
    print("Data insertion complete. Tables 'users' and 'UserRoles' updated successfully.")

insert_data()