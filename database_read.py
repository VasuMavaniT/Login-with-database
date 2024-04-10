import psycopg2

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

# Execute SELECT query to fetch all records
cur.execute("SELECT * FROM UsersData;")

# Fetch all records
records = cur.fetchall()

# Print fetched records
for record in records:
    print(record)

# Close cursor and connection
cur.close()
conn.close()
