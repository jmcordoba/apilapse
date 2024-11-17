"""
blablabla
# https://kb.synology.com/en-uk/DSM/tutorial/Set_up_Python_virtual_environment_on_NAS
# https://medium.com/@rizqinur2010/deploying-python-flask-in-synology-dsm-7-without-docker-d99f1603bc87
"""
import json
#import logging
#import logging.handlers
#from flask import Flask, render_template
from flask import Flask, jsonify, make_response, Response, request
#, request, send_file, redirect, url_for, has_request_context
from src.infra.status import Status
from src.infra.sqlite3 import Database  # Import the Database class

app = Flask(__name__)
#CORS(app)

@app.route("/")
def hello():
    """
    blablabla
    """
    #logger = logging.getLogger()
    #h = logging.handlers.SysLogHandler(address=("jmcordoba.synology.me", 514), facility='user')
    #logger.setLevel(logging.DEBUG)
    #logger.addHandler(h)
    #logger.info('message from main module')
    return "Hello, World!"

@app.route("/v1/status", methods=['GET'])
def v1_status():
    """
    Return the status of the application
    """
    infra_status = Status()
    response = infra_status.get_status(request)
    return Response(
        json.dumps(response),
        status=200,
        mimetype="application/json")

@app.route("/x", methods=['GET'])
def hellox():
    """
    blablabla
    """
    data={
        "code" : 15, 
        "message" : "Data Structures and Algorithms"
    }
    return make_response(jsonify(data),200,{'Access-Control-Allow-Origin':'*'})

@app.route("/db", methods=['POST'])
def db_post():
    """
    blablabla
    """
    # Initialize the database
    db = Database("db/example.db")
    db.create_connection()

    # Insert a new row
    name = request.json.get('name')
    email = request.json.get('email')
    insert_query = "INSERT INTO users (name, email) VALUES (?, ?)"
    db.execute_query(insert_query, (name, email))
    
    #db.close_connection()
    
    return jsonify({"message": "Database initialized and new row inserted"}), 200

@app.route("/db", methods=['GET'])
def db_get():
    """
    blablabla
    """
    # Initialize the database
    db = Database("db/example.db")
    db.create_connection()

    # read all rows
    query = "SELECT * FROM users"
    rows = db.fetch_all(query)

    print(rows)

    db.close_connection()
    
    return jsonify({"message": "Database successfully read"}), 200

#@app.route("/template")
#def template():
    #return render_template('index.html')

if __name__ == "__main__":

    try:
        # Initialize the database
        db = Database("db/example.db")
        db.create_connection()
        
        # Create a table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        );
        """
        db.execute_query(create_table_query)

        # Close connection
        db.close_connection()
    except Exception as e:
        print(f"Error initializing database: {e}")

    # Run the application
    app.run(host='0.0.0.0', debug=False, port=8080)
