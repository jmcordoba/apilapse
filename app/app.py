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
from routes.requests import req
from src.infra.db.init import Db
from src.infra.shared.conf import Config

app = Flask(__name__,
            template_folder='web/templates',
            static_folder='web/static')
app.register_blueprint(hello, url_prefix='')
app.register_blueprint(web, url_prefix='')
app.register_blueprint(health, url_prefix='/health')
app.register_blueprint(ip, url_prefix='/ip/v1')
app.register_blueprint(req, url_prefix='/requests/v1')

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

@app.after_request
def add_security_headers(response):
    """
    Add security headers to the response.
    """
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; '+config['host']
    return response

if __name__ == "__main__":

    # Load the configuration from the Config class
    conf = Config()
    config = conf.get_config()

    # Initialize the database
    database = Db()
    message = database.init()

    # Run the application
    app.run(host=config['host'], debug=config['debug'], port=config['port'])
