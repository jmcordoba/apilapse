from flask import Blueprint, jsonify, request, render_template

template = Blueprint('template', __name__)

@template.route("/template", methods=['GET'])
def v1_template():
    """
    Return a template
    """
    return render_template('index.html')