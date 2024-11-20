from flask import Blueprint, jsonify, request, render_template

web = Blueprint('web', __name__)

@web.route("/", methods=['GET'])
def main():
    """
    Return a template
    """
    return render_template('user/index.html')

@web.route("/signin", methods=['GET'])
def signin():
    """
    Return a template
    """
    return render_template('signin.html')

@web.route("/forgot_password", methods=['GET'])
def forgot_password():
    """
    Return a template
    """
    return render_template('forgot_password.html')

@web.route("/validate", methods=['GET'])
def validate():
    """
    Return a template
    """
    return render_template('validate.html')

@web.route("/home", methods=['GET'])
def home():
    """
    Return a template
    """
    return render_template('home.html')

@web.route("/reset_password", methods=['GET'])
def reset_password():
    """
    Return a template
    """
    return render_template('reset_password.html')
