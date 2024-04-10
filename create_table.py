import psycopg2

# Function to connect to the PostgreSQL database and return the connection and cursor
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

# Function to create the UsersData table
def create_usersdata_table():
    conn, cur = connect_db()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS UsersData (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(50) NOT NULL
    );
    """
    cur.execute(create_table_query)
    print("Table 'UsersData' created successfully.")
    cur.close()
    conn.close()

# Call the function to create the table
create_usersdata_table()
