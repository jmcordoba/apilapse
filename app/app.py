"""
blablabla
# https://kb.synology.com/en-uk/DSM/tutorial/Set_up_Python_virtual_environment_on_NAS
# https://medium.com/@rizqinur2010/deploying-python-flask-in-synology-dsm-7-without-docker-d99f1603bc87
"""
import logging
import logging.handlers
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    """
    blablabla
    """
    logger = logging.getLogger()

    h = logging.handlers.SysLogHandler(address=("jmcordoba.synology.me", 514), facility='user')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(h)
    logger.info('message from main module')

    return "Hello, World!"

@app.route("/x")
def hellox():
    """
    blablabla
    """
    # https://api.twitter.com/2/openapi.json
    return "Hello, X!"
@app.route("/template")
def template():
    """
    blablabla
    """
    return render_template('index.html')