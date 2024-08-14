from flask import Flask, render_template
import logging, logging.handlers

# https://kb.synology.com/en-uk/DSM/tutorial/Set_up_Python_virtual_environment_on_NAS
# https://medium.com/@rizqinur2010/deploying-python-flask-in-synology-dsm-7-without-docker-d99f1603bc87

app = Flask(__name__)

@app.route("/")
def hello():

    logger = logging.getLogger()

    h = logging.handlers.SysLogHandler(address=("jmcordoba.synology.me", 514), facility='user')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(h)
    logger.info('message from main module')

    return "Hello, World!"

@app.route("/x")
def hellox():

    # https://api.twitter.com/2/openapi.json

    return "Hello, X!"
@app.route("/template")
def template():

    return render_template('index.html')
