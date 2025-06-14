from flask import Blueprint, request, render_template

routine_ = Blueprint('routine', __name__, template_folder="./views", static_folder="./static", root_path="./")

@routine_.route("/hello", methods=['GET'])
def teste():
    return "hello!"