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
    dbname="mydatabase",  # Your database name
    user="postgres",      # Default superuser
    password="admin",     # Password for the superuser
    host="localhost"      # Host where PostgreSQL is running
)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()
    return user

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
                return render_template('success.html', username=username)
            else:
                return render_template('login_unsuccess.html')
    
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, port=8097)
