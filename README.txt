
Simple Authentication Web App using Flask + MySQL

SETUP INSTRUCTIONS:

1. Install dependencies:
   pip install flask mysql-connector-python werkzeug

2. Set up MySQL:
   CREATE DATABASE auth_demo;
   USE auth_demo;
   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(150) NOT NULL UNIQUE,
       password VARCHAR(255) NOT NULL
   );

3. Update MySQL credentials in app.py (host, user, password).

4. Run the app:
   python app.py

5. Visit in browser:
   http://127.0.0.1:5000/
