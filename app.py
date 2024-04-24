from flask import Flask, render_template, request, redirect, url_for, session, render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired
import psycopg2
import secrets
import bcrypt
import redis
import logging
from insert_data_final import insert_initial_data
from authlib.integrations.flask_client import OAuth

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = secret_key

# Configure the OAuth client with Auth0 directly with hardcoded values
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id='mqk4sNWNd6yyZk9edcLnL2XJYyWcKJ3R',
    client_secret='Pd9Z6HhgG6RmND6HmTlc__uafXJuo6336131Ib-YO03DX3BvSGxwkQ2lwUcXggp2',
    api_base_url='https://dev-l75eqemhvyb6yxvl.us.auth0.com',
    access_token_url='https://dev-l75eqemhvyb6yxvl.us.auth0.com/oauth/token',
    authorize_url='https://dev-l75eqemhvyb6yxvl.us.auth0.com/authorize',
    client_kwargs={'scope': 'openid profile email'},
    jwks_uri='https://dev-l75eqemhvyb6yxvl.us.auth0.com/.well-known/jwks.json',
)

# Setup Redis
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Register')

def connect_db():
    '''This function is used to connect to the database.'''
    try:
        conn = psycopg2.connect(
            dbname="mydatabase",
            user="postgres",
            password="postgres",
            host="db",
            port=5432
        )
        return conn, conn.cursor()
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None, None

def close_db(conn, cur):
    '''This function is used to close the database connection.'''
    if cur:
        cur.close()
    if conn:
        conn.close()

def hash_password(password):
    """Hash a password for storing."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def authenticate_user(username, password):
    '''This function is used to authenticate a user.'''
    conn, cur = connect_db()
    if conn and cur:
        try:
            cur.execute("SELECT password, role FROM usersdata WHERE username = %s", (username,))
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
    '''This function is used to create a new user.'''
    conn, cur = connect_db()
    if conn and cur:
        try:
            cur.execute("SELECT * FROM usersdata WHERE username = %s", (username,))
            if cur.fetchone() is None:
                hashed_password = hash_password(password).decode('utf-8')
                cur.execute("INSERT INTO usersdata (username, password, role) VALUES (%s, %s, %s);", (username, hashed_password, role))
                conn.commit()
                # Invalidate cache
                redis_client.delete('all_users')
                return True
            else:
                return False
        except psycopg2.Error as e:
            print("Error executing SQL:", e)
        finally:
            close_db(conn, cur)
    return False

def get_all_users():
    '''This function is used to fetch all users.'''
    # Check cache first
    users = redis_client.get('all_users')
    if users:
        # logging.info("Fetching from cache: All Users")
        print("Fetching from cache: All Users")
        return eval(users)

    # Fetch from database if not in cache
    conn, cur = connect_db()
    if conn and cur:
        try:
            cur.execute("SELECT username, role FROM usersdata;")
            users = cur.fetchall()
            redis_client.set('all_users', str(users), ex=3600)  # Cache for 1 hour
            # logging.info("Fetching from database and setting cache: All Users")
            print("Fetching from database and setting cache: All Users")
            return users
        finally:
            close_db(conn, cur)
    return []

def update_user(username, role):
    '''This function is used to update a user.'''
    conn, cur = connect_db()
    if conn and cur:
        try:
            cur.execute("UPDATE usersdata SET role = %s WHERE username = %s;", (role, username))
            conn.commit()
            # Invalidate cache
            redis_client.delete('all_users')
        finally:
            close_db(conn, cur)

def delete_user(username):
    '''This function is used to delete a user.'''
    conn, cur = connect_db()
    if conn and cur:
        try:
            cur.execute("DELETE FROM usersdata WHERE username = %s;", (username,))
            conn.commit()
            # Invalidate cache
            redis_client.delete('all_users')
        finally:
            close_db(conn, cur)

def get_users_by_role(role):
    '''This function is used to fetch users by role.'''
    # Check cache first
    cached_users = redis_client.get(f'users_by_role:{role}')
    if cached_users:
        logging.info(f"Fetching from cache: Users by role {role}")
        return eval(cached_users)

    # Fetch from database if not in cache
    conn, cur = connect_db()
    if conn and cur:
        try:
            cur.execute("SELECT username, role FROM usersdata WHERE role = %s;", (role,))
            users = cur.fetchall()
            redis_client.set(f'users_by_role:{role}', str(users), ex=3600)  # Cache for 1 hour
            logging.info(f"Fetching from database and setting cache: Users by role {role}")
            return users
        finally:
            close_db(conn, cur)
    return []

def verify_password(stored_password, provided_password):
    '''This function is used to verify a password.'''
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

@app.route('/')
def home():
    '''This function is used to render the home page.'''
    # Check and insert data if the table is empty
    conn, cur = connect_db()
    if conn and cur:
        try:
            cur.execute("SELECT COUNT(*) FROM usersdata")
            if cur.fetchone()[0] == 0:
                # Run data insertion in the background
                from threading import Thread
                thread = Thread(target=insert_initial_data)
                thread.start()
        except psycopg2.Error as e:
            print("Database query failed:", e)
        finally:
            close_db(conn, cur)

    # Render the home page
    return render_template('home.html')


@app.route('/view_users')
def view_users():
    '''This function is used to view all users.'''
    users = get_all_users()
    return render_template('view_users.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''This function is used to login using a username and password.'''
    form = LoginForm()
    login_success = True
    if form.validate_on_submit():
        user = authenticate_user(form.username.data, form.password.data)
        if user:
            return redirect(url_for('dashboard', username=user[0], role=user[1]))
        else:
            login_success = False
    return render_template('login.html', form=form, login_success=login_success)

@app.route('/login_using_sso', methods=['GET', 'POST'])
def login_using_sso():
    '''This function is used to login using Auth0 SSO.'''
    # Ensure that the callback URL matches exactly what is expected
    callback_url = url_for('callback', _external=True, _scheme='https')  # Use _scheme if running over HTTP
    print("Callback URL:", callback_url)  # This will help confirm the right URL is generated
    return auth0.authorize_redirect(redirect_uri=callback_url)

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''This function is used to register a new user.'''
    form = RegistrationForm()
    if form.validate_on_submit():
        if create_new_user(form.username.data, form.password.data):
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
def dashboard():
    '''This function is used to render the dashboard based on the role of the user.'''
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

@app.route('/admin_profile')
def admin_profile_management():
    '''This function is used to render the admin profile page.'''
    return render_template('admin_profile.html')

@app.route('/admin_notifications')
def admin_notification_management():
    '''This function is used to render the admin notifications page.'''
    return render_template('admin_notifications.html')

@app.route('/admin_logs')
def admin_logs_management():
    '''This function is used to render the admin logs page.'''
    return render_template('admin_logs.html')

@app.route('/admin_manage', methods=['GET', 'POST'])
def admin_manage():
    '''This function is used to manage users by the admin.'''
    users = []  # Initialize an empty list for users
    selected_role = None  # Keep track of the selected role for deletion
    roles = ['admin', 'developer', 'user']  # Assuming these are your roles
    is_delete = False
    is_update = False

    # Fetch users for display
    users = get_all_users()  # Fetch all users for display

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            create_new_user(request.form.get('new-username'), request.form.get('new-password'), request.form.get('new-role'))        
        elif action == 'update':
            is_update = True
            selected_role = request.form.get('role')
            if selected_role:
                users = get_users_by_role(selected_role)  # Fetch users of the selected role
        elif action == 'perform_update':
            username = request.form.get('username')
            role = request.form.get('new_role') # Get the new role
            if username and role:
                update_user(username, role)
                return redirect(url_for('admin_manage'))
        elif action == 'delete':
            users = get_all_users()  # Fetch all users for display
            usernames = request.form.getlist('usernames[]')  # Get list of selected usernames
            if usernames:
                for username in usernames:
                    delete_user(username)  # Perform deletion for each selected user
                return redirect(url_for('admin_manage'))

    return render_template('admin_manage.html', users=users, roles=roles, selected_role=selected_role, is_delete=is_delete, is_update=is_update)

# Callback route
@app.route('/callback')
def callback():
    '''This function is used to handle the callback from Auth0 after successful authentication.'''
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()
    print("User Info:", userinfo)  # Debug: Check what userinfo contains
    # session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    # Store the email address in the database
    email = userinfo['email']
    password = 'password'  # Example password, should not be hardcoded in production
    print('email: ', email)
    create_new_user(email, password, 'user')
    # Redirect to the dashboard with the correct role
    return redirect(url_for('dashboard', username=email, role='user'))


@app.route('/admin_settings')
def admin_settings_management():
    '''This function is used to render the admin settings page.'''
    return render_template('admin_settings.html')

@app.route('/admin_reports')
def admin_reports_viwers():
    '''This function is used to render the admin reports page.'''
    return render_template('admin_reports.html')

@app.route('/developer_profile')
def developer_profile_management():
    '''This function is used to render the developer profile page.'''
    return render_template('developer_profile.html')

@app.route('/developer_notifications')
def developer_notifications_management():
    '''This function is used to render the developer notifications page.'''
    return render_template('developer_notifications.html')

@app.route('/developer_logs')
def developer_logs_management():
    '''This function is used to render the developer logs page.'''
    return render_template('developer_logs.html')

@app.route('/user_profile')
def user_profile_management():
    '''This function is used to render the user profile page.'''
    return render_template('user_profile.html')

@app.route('/user_notifications')
def user_notifications_management():
    '''This function is used to render the user notifications page.'''
    return render_template('user_notifications.html')

@app.route('/documentation')
def documentation():
    '''This function is used to render the documentation page.'''
    return render_template('documentation.html')

@app.route('/show_all_users')
def show_all_users():
    '''This function is used to render the show all users page.'''
    users = get_all_users()
    return render_template('show_all_users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True, port=8097)