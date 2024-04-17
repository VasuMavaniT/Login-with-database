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
    drop_table_query = "DROP TABLE IF EXISTS usersdata;"

    # Execute the SQL statement
    cur.execute(drop_table_query)

    # Commit the transaction
    conn.commit()

    print("Table 'usersdata' deleted successfully")

except psycopg2.Error as e:
    print("Error deleting table:", e)

finally:
    # Close the cursor and connection
    if cur:
        cur.close()
    if conn:
        conn.close()
