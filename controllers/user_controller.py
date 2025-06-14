from flask import Blueprint, request, render_template

user_ = Blueprint('user', __name__, template_folder="./views", static_folder="./static", root_path="./")

@user_.route("/hello", methods=['GET'])
def teste():
    return "hello!"