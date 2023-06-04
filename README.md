# simple-flask-app
A flask app that connects to a MySql database and performs CRUD operations on a table called "users". <br>
```user_app.py``` implements the basic server without error handling, while ```user_app2.py``` implements error handling.
Steps for installation and setup:
- Run the command ```$ pip install -r requirements.txt``` or install the python dependencies for the app manually.
- Start the mysql server and set up the database as shown in db_setup.png.
- In the file ```user_app.py``` or ```user_app2.py```, set the app config parameters on lines 6 - 10 (like hostname, mysql username and password, mysql port number and database name) as per the configuration on your local machine.
- Run the command ```$ python user_app.py``` or ```$ python user_app2.py``` to start the server. The server runs on 'localhost' at port 5000 by default. Set host='0.0.0.0' as the argument of app.run() function on the last line to expose the api endpoints (make them avaiable externally). Enable debug option to view the logs of the requests made to the server.
- Test the api operations using a REST client like Postman.
