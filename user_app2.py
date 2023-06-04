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
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        users = []
        for row in data:
            user = {
                'id': row[0],
                'name': row[1],
                'email': row[2]
            }
            users.append(user)
        return jsonify(users=users)
    except:
        return jsonify(error="Database error"), 500
    finally:
        if cur:
            cur.close() 

@app.route('/users/<int:id>', methods=['GET'])
def getUser(id):
    try:
        cur = mysql.connection.cursor()

        # Invalid user id
        if int(id) <= 0:
            return jsonify(error="Invalid user id. User id must be positive.")
        
        cur.execute("SELECT * FROM users WHERE id = %s", (id,))
        data = cur.fetchone()
        if data is None:
            return jsonify(error="No such user in database"), 404
        return jsonify(data)
    except ValueError:
        return jsonify(error="Invalid user id. User id must be integer."), 400
    except:
        return jsonify(error="Database error"), 500
    finally:
        if cur:
            cur.close() 

@app.route('/users', methods=['POST'])
def createUser():
    try:
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()

        # Invalid user id
        user_id = int(request.form['id'])
        if user_id <= 0:
            return jsonify(error="Invalid user id. User id must be positive.")

        # Check for existing user id
        cur.execute("SELECT * FROM users WHERE id = %s", (id,))
        data = cur.fetchone()
        if data is not None:
            return jsonify(error="User already exists. Please use a different user id.")
        
        # Check for existing user name
        # cur.execute("SELECT * FROM users WHERE name = %s", (name,))
        # data = cur.fetchone()
        # if data is not None:
        #     return jsonify(error="User already exists. Please use a different user name to avoid duplicate user creation.")
        
        cur.execute("INSERT INTO users (id, name, email) VALUES (%s, %s, %s)", (id, name, email))
        mysql.connection.commit()
        return "Succesfully inserted user " + str(name) + " with email " + str(email) + " and id " + str(id) + " into users table"
    except ValueError:
        return jsonify(error="Invalid user id. User id must be integer."), 400
    except:
        return jsonify(error="Database error"), 500
    finally:
        if cur:
            cur.close() 

@app.route('/users/<int:id>', methods=['PUT'])
def updateUser(id):
    try:
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()

        # Invalid user id
        user_id = int(request.form['id'])
        if user_id <= 0:
            return jsonify(error="Invalid user id. User id must be positive.")

        # Check for existing user id
        cur.execute("SELECT * FROM users WHERE id = %s", (id,))
        data = cur.fetchone()
        if data is None:
            return jsonify(error="User does not exist."), 404
        
        if name == "":
            cur.execute("UPDATE users SET email = %s WHERE id = %s", (email, id))
        elif email == "":
            cur.execute("UPDATE users SET name = %s WHERE id = %s", (name, id))
        else:
            cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, id))
        mysql.connection.commit()
        return "Successfully updated user " + str(id) + " with new name as " + str(name) + " and new email as " + str(email)
    except ValueError:
        return jsonify(error="Invalid user id. User id must be integer."), 400
    except:
        return jsonify(error="Database error"), 500
    finally:
        if cur:
            cur.close() 

@app.route('/users/<int:id>', methods=['DELETE'])
def deleteUser(id):
    try:
        cur = mysql.connection.cursor()

        # Invalid user id
        if int(id) <= 0:
            return jsonify(error="Invalid user id. User id must be positive.")
        
        # Check for existing user id
        cur.execute("SELECT * FROM users WHERE id = %s", (id,))
        data = cur.fetchone()
        if data is None:
            return jsonify(error="User does not exist."), 404
        
        cur.execute("DELETE FROM users WHERE id = %s", (id,))
        mysql.connection.commit()
        return "Succesfully deleted user " + str(id) + " from users table"
    except ValueError:
        return jsonify(error="Invalid user id. User id must be integer."), 400
    except:
        return jsonify(error="Database error"), 500
    finally:
        if cur:
            cur.close() 

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
