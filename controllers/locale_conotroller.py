from flask import Blueprint, request, render_template

locale_ = Blueprint('locale', __name__, template_folder="./views", static_folder="./static", root_path="./")

@locale_.route("/hello", methods=['GET'])
def teste():
    return "hello!"