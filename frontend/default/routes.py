from config import Config
from flask import Blueprint
from flask import render_template

default_bp = Blueprint("default_bp", __name__, template_folder="templates")


@default_bp.route("/")
def index():
    """
    An example route
    :return: HTML Index page
    """
    from external_services.data import get_data

    endpoint = Config.FUND_STORE_API_HOST + Config.FUNDS_ENDPOINT
    funds = get_data(endpoint)

    return render_template("index.html", funds=funds)


@default_bp.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@default_bp.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500
