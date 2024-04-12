import psycopg2

# Function to connect to the PostgreSQL database and return the connection and cursor
def connect_db():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="admin",
        host="localhost"
    )
    conn.autocommit = True
    cur = conn.cursor()
    return conn, cur

def create_usersdata_table():
    conn, cur = connect_db()
    create_table_query = """
    CREATE TABLE usersdata (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL
    );
    """


    cur.execute(create_table_query)
    print("Table 'usersdata' created successfully.")
    cur.close()
    conn.close()


# Call the function to create the table
create_usersdata_table()
