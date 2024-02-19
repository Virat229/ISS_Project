import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Database connection parameters
db_host = 'localhost'  # Change this to your MySQL server host
db_user = 'root'  # Change this to your MySQL username
db_password = 'Khwaish@1237'  # Change this to your MySQL password
db_name = 'sys'  # Change this to your MySQL database name

# Function to create a database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to MySQL database:", e)
        return None

# Route for the signup page
@app.route('/')
def signup():
    return render_template('signup.html')

# Route for handling signup form submission
@app.route('/signup', methods=['POST'])
def signup_submit():
    username = request.form['username']
    password = request.form['password']
    
    # Check if the user already exists in the database
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Check if the username already exists
            cursor.execute("SELECT * FROM user_login WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                cursor.close()
                conn.close()
                return 'Username already exists. Please choose a different one.'
            else:
                # Insert data into the user_login table
                cursor.execute("INSERT INTO user_login(username, password) VALUES (%s, %s)", (username, password))
                conn.commit()
                cursor.close()
                conn.close()
                # Redirect to login.html after successful signup
                return redirect(url_for('login'))
        except mysql.connector.Error as e:
            print("Error executing SQL query:", e)
            return 'Error storing user data in the database.'
    else:
        return 'Error connecting to the database.'

# Route for the login page
@app.route('/login')
def login():
    return render_template('login.html')

# Route for handling login form submission
@app.route('/login', methods=['POST'])
def login_submit():
    username = request.form['username']
    password = request.form['password']
    
    # Check if the user exists in the database
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Check if the username and password match a record in the database
            cursor.execute("SELECT * FROM user_login WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            if user:
                cursor.close()
                conn.close()
                # Redirect to dropbox.html after successful login
                return redirect(url_for('dropbox'))
            else:
                return 'Invalid username or password. Please sign up first.'
        except mysql.connector.Error as e:
            print("Error executing SQL query:", e)
            return 'Error retrieving user data from the database.'
    else:
        return 'Error connecting to the database.'

# Route for dropbox.html
@app.route('/dropbox')
def dropbox():
    return render_template('dropbox.html')

if __name__ == '__main__':
    app.run(debug=True)