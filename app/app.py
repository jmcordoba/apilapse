"""
blablabla
# https://kb.synology.com/en-uk/DSM/tutorial/Set_up_Python_virtual_environment_on_NAS
# https://medium.com/@rizqinur2010/deploying-python-flask-in-synology-dsm-7-without-docker-d99f1603bc87
"""
import json
import os
import sqlite3
import logging
from flask import Flask, jsonify, make_response, Response, request, current_app
from src.infra.status import Status
from src.infra.sqlite3 import Database
from src.infra.user.create import UserCreate
from src.infra.user.get import UserGet

app = Flask(__name__)

# Purge the log file
LOG_FILE = 'app.log'
with open(LOG_FILE, 'w', encoding='utf-8'):
    pass

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        logging.FileHandler(LOG_FILE),
                        logging.StreamHandler()
                    ])

@app.route("/")
def hello():
    """
    blablabla
    """

    current_app.logger.info('Showing the hello message')
    current_app.logger.warning('Showing the hello message')
    current_app.logger.debug('Showing the hello message')
    current_app.logger.error('Showing the hello message')

    data={
        "message" : "Hello, World!"
    }
    return jsonify(data), 200, {'Access-Control-Allow-Origin':'*'}

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

    user_create = UserCreate()
    message = user_create.insert_user()

    return jsonify({"message": message}), 200

@app.route("/db", methods=['GET'])
def db_get():
    """
    blablabla
    """

    user_get = UserGet()
    rows = user_get.get_users()

    return jsonify({"rows": rows}), 200

#@app.route("/template")
#def template():
    #return render_template('index.html')

if __name__ == "__main__":

    try:
        # Set the configuration file path
        JSON_CONFIG = 'conf/dev.json'

        # Load the configuration from file
        with open(JSON_CONFIG, 'r', encoding='utf-8') as file:
            config = json.load(file)
            for key, value in config.items():
                os.environ[key] = value

        # Get the database name from the environment and Initialize the database
        db = Database(os.getenv('database_name'))
        db.create_connection()

        # Create a table if it doesn't exist
        QUERY = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        );
        """
        db.execute_query(QUERY)

        # Close connection
        db.close_connection()
    except FileNotFoundError as e:
        print(f"Configuration file not found: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    # Run the application
    app.run(host='0.0.0.0', debug=True, port=8080)
