from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired
import psycopg2
import secrets
import bcrypt

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = secret_key

def hash_password(password):
    """Hash a password for storing."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')

def authenticate_user(username, password):
    conn, cur = connect_db()
    if conn and cur:
        try:
            cur.execute("SELECT password, role FROM UsersData WHERE username = %s", (username,))
            user_record = cur.fetchone()
            if user_record:
                stored_password, user_role = user_record
                # Convert the stored password from string to bytes
                stored_password_bytes = stored_password.encode('utf-8')
                # Convert the provided password to bytes
                provided_password_bytes = password.encode('utf-8')
                # Use bcrypt's checkpw method to compare the provided password with the stored hash
                if bcrypt.checkpw(provided_password_bytes, stored_password_bytes):
                    # If the passwords match, return the username and role
                    return username, user_role
            # If authentication fails, return None
            return None
        except psycopg2.Error as e:
            print("Error executing SQL query:", e)
        finally:
            close_db(conn, cur)
    # If database connection fails, return None
    return None

def close_db(conn, cur):
    if cur:
        cur.close()
    if conn:
        conn.close()

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="mydatabase",
            user="postgres",
            password="admin",
            host="localhost"
        )
        return conn, conn.cursor()
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None, None
    
    

# def check_credentials(username, password):
#     # Connect to PostgreSQL server
#     conn = psycopg2.connect(
#         dbname="mydatabase",
#         user="postgres",
#         password="admin",
#         host="localhost"
#     )
#     cur = conn.cursor()
#     cur.execute("SELECT username, role FROM UsersData WHERE username = %s AND password = %s", (username, password))
#     user = cur.fetchone()
#     cur.close()
#     return user

def create_new_user(username, password, role):
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="postgres",
        password="admin",
        host="localhost"
    )

    # Check if the username already exists and if not exists, insert the new user
    cur = conn.cursor()
    cur.execute("SELECT * FROM UsersData WHERE username =%s", (username,))
    user = cur.fetchone()
    if user:
        flash('Username already exists!', 'error')
    else:
        temp = hash_password(password)
        hashed_password = temp.decode('utf-8')
        cur.execute("INSERT INTO UsersData (username, password, role) VALUES (%s, %s, %s);", (username, hashed_password, role))
        conn.commit()
        flash('User created successfully!', 'success')
    cur.close()
    conn.close()
    

def get_all_users():
    # This function fetches all users from the database and returns them
    conn = psycopg2.connect(dbname="mydatabase", user="postgres", password="admin", host="localhost")
    cur = conn.cursor()
    cur.execute("SELECT username, role FROM UsersData;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def update_user(username, role):
    conn = psycopg2.connect(dbname="mydatabase", user="postgres", password="admin", host="localhost")
    cur = conn.cursor()
    cur.execute("UPDATE UsersData SET role = %s WHERE username = %s;", (role, username))
    conn.commit()
    cur.close()
    conn.close()

def delete_user(username):
    conn = psycopg2.connect(dbname="mydatabase", user="postgres", password="admin", host="localhost")
    cur = conn.cursor()
    cur.execute("DELETE FROM UsersData WHERE username = %s;", (username,))
    conn.commit()
    cur.close()
    conn.close()

def get_users_by_role(role):
    conn = psycopg2.connect(dbname="mydatabase", user="postgres", password="admin", host="localhost")
    cur = conn.cursor()
    cur.execute("SELECT username, role FROM UsersData WHERE role = %s;", (role,))
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Process the form data
        username = form.username.data
        password = form.password.data
        
        # Check if either username or password is missing
        if not username or not password:
            flash('Invalid username or password.', 'error')
        else:
            user = authenticate_user(username, password)
            if user:
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard', username=user[0], role=user[1]))
            else:
                flash('Invalid username or password.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    username = request.args.get('username')
    role = request.args.get('role')

    if role == 'admin':
        return render_template('admin_dashboard.html', username=username)
    elif role == 'developer':
        return render_template('developer_dashboard.html', username=username)
    elif role == 'user':
        return render_template('end_user_dashboard.html', username=username)
    else:
        return 'Role not recognized!', 403
    
@app.route('/admin1')
def admin1():
    # You might want to check the user's role and take appropriate action
    return render_template('admin1.html')

@app.route('/admin2')
def admin2():
    # You might want to check the user's role and take appropriate action
    return render_template('admin2.html')

@app.route('/admin3')
def admin3():
    # You might want to check the user's role and take appropriate action
    return render_template('admin3.html')

@app.route('/admin4', methods=['GET', 'POST'])
def assign_role():
    users = []  # Initialize an empty list for users
    selected_role = None  # Keep track of the selected role for deletion
    roles = ['admin', 'developer', 'user']  # Assuming these are your roles
    is_delete = False
    is_update = False

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            create_new_user(request.form.get('username'), request.form.get('password'), request.form.get('role'))        
        if action == 'update':
            is_update = True
            selected_role = request.form.get('role')
            if selected_role:
                users = get_users_by_role(selected_role)  # Fetch users of the selected role
        elif action == 'perform_update':
            username = request.form.get('username')
            role = request.form.get('new_role') # Get the new role
            if username and role:
                update_user(username, role)
                return redirect(url_for('assign_role'))
        elif action == 'delete':
            is_delete = True
            selected_role = request.form.get('role')
            if selected_role:
                users = get_users_by_role(selected_role)  # Fetch users of the selected role
        elif action == 'perform_delete':
            username = request.form.get('username')
            if username:
                delete_user(username)  # Perform the deletion
                return redirect(url_for('assign_role'))

    return render_template('assign_role.html', users=users, roles=roles, selected_role=selected_role, is_delete=is_delete, is_update=is_update)

@app.route('/admin5')
def admin5():
    return render_template('admin5.html')

@app.route('/admin6')
def admin6():
    return render_template('admin6.html')

@app.route('/developer1')
def developer1():
    return render_template('developer1.html')

@app.route('/developer2')
def developer2():
    return render_template('developer2.html')

@app.route('/developer3')
def developer3():
    return render_template('developer3.html')

@app.route('/user1')
def user1():
    return render_template('user1.html')

@app.route('/user2')
def user2():
    return render_template('user2.html')

@app.route('/show_all_users')
def show_all_users():
    users = get_all_users()  # Reuse the existing function to fetch all users
    return render_template('show_all_users.html', users=users)

def verify_password(stored_password, provided_password):
    # Convert the provided password to bytes
    provided_password_bytes = provided_password.encode('utf-8')
    # Use bcrypt's checkpw method to compare the passwords
    if bcrypt.checkpw(provided_password_bytes, stored_password):
        return True
    else:
        return False

if __name__ == '__main__':
    app.run(debug=True, port=8097)
