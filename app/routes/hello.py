from flask import Blueprint, jsonify, current_app

hello = Blueprint('hello', __name__)

@hello.route("/hello", methods=['GET'])
def v1_hello():
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
