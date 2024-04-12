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

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Register')

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

def close_db(conn, cur):
    if cur:
        cur.close()
    if conn:
        conn.close()

def hash_password(password):
    """Hash a password for storing."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def authenticate_user(username, password):
    conn, cur = connect_db()
    if conn and cur:
        try:
            cur.execute("SELECT password, role FROM UsersData WHERE username = %s", (username,))
            user_record = cur.fetchone()
            if user_record:
                stored_password, user_role = user_record
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    return username, user_role
            return None
        except psycopg2.Error as e:
            print("Error executing SQL query:", e)
        finally:
            close_db(conn, cur)
    return None

def create_new_user(username, password, role='user'):
    conn, cur = connect_db()
    if conn and cur:
        try:
            cur.execute("SELECT * FROM UsersData WHERE username = %s", (username,))
            if cur.fetchone() is None:
                hashed_password = hash_password(password).decode('utf-8')
                cur.execute("INSERT INTO UsersData (username, password, role) VALUES (%s, %s, %s);", (username, hashed_password, role))
                conn.commit()
                flash('User created successfully!', 'success')
                return True
            else:
                flash('Username already exists!', 'error')
                return False
        except psycopg2.Error as e:
            print("Error executing SQL:", e)
        finally:
            close_db(conn, cur)
    return False

def get_all_users():
    conn, cur = connect_db()
    if conn and cur:
        try:
            cur.execute("SELECT username, role FROM UsersData;")
            users = cur.fetchall()
            return users
        finally:
            close_db(conn, cur)
    return []

def update_user(username, role):
    conn, cur = connect_db()
    if conn and cur:
        try:
            cur.execute("UPDATE UsersData SET role = %s WHERE username = %s;", (role, username))
            conn.commit()
        finally:
            close_db(conn, cur)

def delete_user(username):
    conn, cur = connect_db()
    if conn and cur:
        try:
            cur.execute("DELETE FROM UsersData WHERE username = %s;", (username,))
            conn.commit()
        finally:
            close_db(conn, cur)

def get_users_by_role(role):
    conn, cur = connect_db()
    if conn and cur:
        try:
            cur.execute("SELECT username, role FROM UsersData WHERE role = %s;", (role,))
            users = cur.fetchall()
            return users
        finally:
            close_db(conn, cur)
    return []

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate_user(form.username.data, form.password.data)
        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard', username=user[0], role=user[1]))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if create_new_user(form.username.data, form.password.data):
            flash('Registration successful! You can now login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists! Try a different one.', 'error')
    return render_template('register.html', form=form)

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
    return render_template('admin1.html')

@app.route('/admin2')
def admin2():
    return render_template('admin2.html')

@app.route('/admin3')
def admin3():
    return render_template('admin3.html')

@app.route('/admin4', methods=['GET', 'POST'])
def assign_role():
    users = get_all_users()
    roles = ['admin', 'developer', 'user']
    if request.method == 'POST':
        action = request.form.get('action')
        selected_role = request.form.get('role')
        if action == 'create':
            create_new_user(request.form.get('username'), request.form.get('password'), request.form.get('role'))
        elif action == 'update':
            update_user(request.form.get('username'), request.form.get('role'))
        elif action == 'delete':
            delete_user(request.form.get('username'))
    return render_template('assign_role.html', users=users, roles=roles)

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
    users = get_all_users()
    return render_template('show_all_users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True, port=8097)
