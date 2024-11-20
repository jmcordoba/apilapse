"""
blablabla
# https://kb.synology.com/en-uk/DSM/tutorial/Set_up_Python_virtual_environment_on_NAS
# https://medium.com/@rizqinur2010/deploying-python-flask-in-synology-dsm-7-without-docker-d99f1603bc87
"""
import logging
from flask import Flask
from routes.health import health
from routes.hello import hello
from routes.web import web
from routes.identity_provider import ip
from src.infra.db.init import Db

app = Flask(__name__,
            template_folder='web/templates',
            static_folder='web/static')
app.register_blueprint(hello, url_prefix='')
app.register_blueprint(web, url_prefix='')
app.register_blueprint(health, url_prefix='/health')
app.register_blueprint(ip, url_prefix='/ip/v1')

# Purge the log file
LOG_FILE = 'logs/app.log'
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

if __name__ == "__main__":

    # Initialize the database
    database = Db()
    message = database.init()

    # Run the application
    app.run(host='0.0.0.0', debug=True, port=8080)
