"""
blablabla
# https://kb.synology.com/en-uk/DSM/tutorial/Set_up_Python_virtual_environment_on_NAS
# https://medium.com/@rizqinur2010/deploying-python-flask-in-synology-dsm-7-without-docker-d99f1603bc87
"""
#import logging
#import logging.handlers
#from flask import Flask, render_template
from flask import Flask, jsonify, make_response
#, request, send_file, redirect, url_for, Response, has_request_context
#from flask_cors import CORS

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

@app.route("/x", methods=['GET'])
def hellox():
    """
    blablabla
    # https://api.twitter.com/2/openapi.json
    """
    data={
        "code" : 15, 
        "message" : "Data Structures and Algorithms", 
    }
    return make_response(jsonify(data), 200)

#@app.route("/template")
#def template():
    #return render_template('index.html')

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=8080)
    #app.run(host='0.0.0.0')
