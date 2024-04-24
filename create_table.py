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

def create_tables():
    conn, cur = connect_db()
    
    try:
        # Create the Users table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            userid VARCHAR(20) PRIMARY KEY,
            username VARCHAR(20) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        """)
        print("Table 'Users' created successfully.")

        # Create the Roles table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Roles (
            roleid VARCHAR(20) PRIMARY KEY,
            rolename VARCHAR(20) UNIQUE NOT NULL
        );
        """)
        print("Table 'Roles' created successfully.")
        
        # Create the UserRoles table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS UserRoles (
            userid VARCHAR(20) REFERENCES Users(userid),
            roleid VARCHAR(20) REFERENCES Roles(roleid),
            PRIMARY KEY (userid, roleid)
        );
        """)
        print("Table 'UserRoles' created successfully.")
    except psycopg2.Error as e:
        print("An error occurred: ", e)
    finally:
        # Ensure to close cursor and connection
        cur.close()
        conn.close()

create_tables()
