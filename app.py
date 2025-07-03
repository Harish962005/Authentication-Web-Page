from flask import Flask, render_template, request, redirect, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)



def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="XXXXXXX",
        database="authentication",
        buffered=True   
    )

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']
        password_hashed = generate_password_hash(password_input)

        print("Generated hash:", password_hashed)  

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password_hashed))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/login')
        except Exception as e:
            return f"Error inserting user: {e}"

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user WHERE username=%s", (username,))
            user = cursor.fetchone()

            print("Fetched user:", user)  
            print(" Password input:", password_input)

            cursor.close()
            conn.close()

            if user:
                print(" Stored hash:", user['password'])
                print("Match result:", check_password_hash(user['password'], password_input))

            if user and check_password_hash(user['password'], password_input):
                session['user'] = user['username']
                return redirect('/dashboard')
            else:
                return render_template('login.html', error="Invalid credentials!")

        except Exception as e:
            return f"Login error: {e}"

    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
