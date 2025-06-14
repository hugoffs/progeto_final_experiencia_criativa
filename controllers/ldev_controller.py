from flask import Blueprint, request, render_template

ldev_ = Blueprint('ldev', __name__, template_folder="./views", static_folder="./static", root_path="./")

@ldev_.route("/hello", methods=['GET'])
def teste():
    return "hello!"