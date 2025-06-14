from flask import Blueprint, request, render_template

team_ = Blueprint('team', __name__, template_folder="./views", static_folder="./static", root_path="./")

@team_.route("/hello", methods=['GET'])
def teste():
    return "hello!"