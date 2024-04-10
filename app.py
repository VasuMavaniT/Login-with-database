from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired
import psycopg2
import secrets

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = secret_key

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')

def check_credentials(username, password):
    # Connect to PostgreSQL server
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="postgres",
        password="admin",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute("SELECT username, role FROM UsersData WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()
    return user

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
        cur.execute("INSERT INTO UsersData (username, password, role) VALUES (%s, %s, %s);", (username, password, role))
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
        if not username:
            flash('Username is required.', 'error')
        elif not password:
            flash('Password is required.', 'error')
        else:
            # Check credentials
            user = check_credentials(username, password)
            if user:
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard', username=user[0], role=user[1]))
            else:
                return render_template('login_unsuccess.html')
    
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    username = request.args.get('username')
    role = request.args.get('role')

    if role == 'admin':
        return render_template('admin_dashboard.html', username=username)
    elif role == 'developer':
        return render_template('developer_dashboard.html', username=username)
    elif role == 'end_user':
        return render_template('end_user_dashboard.html', username=username)
    else:
        return 'Role not recognized!', 403
    
@app.route('/template1')
def template1():
    # You might want to check the user's role and take appropriate action
    return render_template('template1.html')

@app.route('/template2')
def template2():
    # You might want to check the user's role and take appropriate action
    return render_template('template2.html')

@app.route('/template3')
def template3():
    # You might want to check the user's role and take appropriate action
    return render_template('template3.html')

@app.route('/template4')
def template4():
    # You might want to check the user's role and take appropriate action
    return render_template('template4.html')

@app.route('/template5')
def template5():
    # You might want to check the user's role and take appropriate action
    return render_template('template5.html')

@app.route('/assign_role', methods=['GET', 'POST'])
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




if __name__ == '__main__':
    app.run(debug=True, port=8097)
