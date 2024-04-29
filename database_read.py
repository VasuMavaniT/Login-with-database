import psycopg2

def connect_db():
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="postgres",
        password="admin",
        host="localhost"
    )
    conn.autocommit = True
    cur = conn.cursor()
    return conn, cur

def read_data_from_userroles():
    conn, cur = connect_db()
    # Execute SELECT query to fetch all records
    cur.execute("SELECT * FROM UserRoles;")

    # Fetch all records
    records = cur.fetchall()

    # Print fetched records
    for record in records:
        print(record)

    # Close cursor and connection
    cur.close()
    conn.close()

def read_data_from_users():
    conn, cur = connect_db()
    # Execute SELECT query to fetch all records
    cur.execute("SELECT * FROM Users;")

    # Fetch all records
    records = cur.fetchall()

    # Print fetched records
    for record in records:
        print(record)

    # Close cursor and connection
    cur.close()
    conn.close()

def read_data_from_roles():
    conn, cur = connect_db()
    # Execute SELECT query to fetch all records
    cur.execute("SELECT * FROM Roles;")

    # Fetch all records
    records = cur.fetchall()

    # Print fetched records
    for record in records:
        print(record)

    # Close cursor and connection
    cur.close()
    conn.close()

read_data_from_userroles()
print("\n\n\n\n\n\n\n")
read_data_from_users()
print("\n\n\n\n\n\n\n")
read_data_from_roles()