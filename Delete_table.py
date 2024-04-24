import psycopg2

try:
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="postgres",
        password="admin",
        host="localhost"
    )

    # Create a cursor object using the connection
    cur = conn.cursor()

    # SQL statement to drop the table
    drop_usersdata = "DROP TABLE IF EXISTS usersdata;"
    drop_users = "DROP TABLE IF EXISTS users;"
    drop_roles = "DROP TABLE IF EXISTS roles;"
    drop_userroles = "DROP TABLE IF EXISTS userroles;"

    # Execute the SQL statement
    cur.execute(drop_usersdata)
    cur.execute(drop_userroles)
    cur.execute(drop_users)
    cur.execute(drop_roles)

    # Commit the transaction
    conn.commit()

    print("Tables are deleted successfully.")

except psycopg2.Error as e:
    print("Error deleting table:", e)

finally:
    # Close the cursor and connection
    if cur:
        cur.close()
    if conn:
        conn.close()
