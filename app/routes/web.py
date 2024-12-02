from flask import Blueprint, jsonify, request, render_template

web = Blueprint('web', __name__)

@web.route("/", methods=['GET'])
def main():
    """
    Return a template
    """
    return render_template('user/index.html')

@web.route("/login", methods=['GET'])
def login():
    """
    Return a template
    """
    return render_template('user/login.html')

@web.route("/signup", methods=['GET'])
def signup():
    """
    Return a template
    """
    return render_template('user/signup.html')

@web.route("/forgot_password", methods=['GET'])
def forgot_password():
    """
    Return a template
    """
    return render_template('user/forgot_password.html')

@web.route("/validate", methods=['GET'])
def validate():
    """
    Return a template
    """
    return render_template('user/validate.html')

@web.route("/reset_password", methods=['GET'])
def reset_password():
    """
    Return a template
    """
    return render_template('user/reset_password.html')

@web.route("/home", methods=['GET'])
def home():
    """
    Return a template
    """
    return render_template('account/home.html')

@web.route("/requests", methods=['GET'])
def requests_list():
    """
    Return the list of requests
    """
    return render_template('requests/list.html')
