from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'guest'
app.config['MYSQL_PASSWORD'] = 'guest'
app.config['MYSQL_DB'] = 'health'
app.config['MYSQL_DATABASE_PORT'] = 3306
 
mysql = MySQL(app)

# cursor = mysql.connection.cursor()
# cursor.execute(''' CREATE TABLE IF NOT EXISTS users(id int, name varchar(255), email varchar(255)) ''')
# cursor.close()

@app.route('/')
def home():
    return "Welcome to the home page! <br> Click here to see a list of all users: <a href='/users/'>User List</a>"

@app.route('/users/', methods=['GET'])
def getAllUsers():
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT * FROM users ''')
    data = cur.fetchall()
    cur.close()
    users = []
    for row in data:
        user = {
            'id': row[0],
            'name': row[1],
            'email': row[2]
        }
        users.append(user)
    return jsonify(users=users)

@app.route('/users/<int:id>', methods=['GET'])
def getUser(id):
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT * FROM users WHERE id = %s ''', (id,))
    data = cur.fetchone()
    cur.close()
    if data is None:
        return "No such user in database"
    return jsonify(data)

@app.route('/users', methods=['POST'])
def createUser():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (id, name, email) VALUES (%s, %s, %s)", (id, name, email))
        mysql.connection.commit()
        cur.close()
        return "Succesfully inserted user " + str(name) + " with email " + str(email) + " and id " + str(id) + " into users table"

@app.route('/users/<int:id>', methods=['PUT'])
def updateUser(id):
    if request.method == 'PUT':
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, id))
        mysql.connection.commit()
        cur.close()
        return "Successfully updated user " + str(id) + " with new name as " + str(name) + " and new email as " + str(email)

@app.route('/users/<int:id>', methods=['DELETE'])
def deleteUser(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return "Succesfully deleted user " + str(id) + " from users table"

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
