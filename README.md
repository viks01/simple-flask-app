# simple-flask-app
A flask app that connects to a MySql database and performs CRUD operations on a table called "users".
Steps for installation and setup:
- Run the command ```$ pip install -r requirements.txt``` or install the python dependencies for the app manually
- Start the mysql server and set up the database as shown in db_setup.png
- In the file user_app.py, set the app config parameters (like hostname, mysql username and password, mysql port number and database name) as per the configuration on your local machine
- Run the command ```$ python user_app.py``` to start the server. The server runs on 'localhost' at port 5000 by default. Set host='0.0.0.0' to expose the api endpoints (make them avaiable externally)
- Test the api operations using a REST client like Postman.
