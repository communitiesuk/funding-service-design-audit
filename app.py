import connexion
from config import Config
from connexion.resolver import MethodViewResolver
from flask import Flask
from flask import request
from flask_assets import Environment
from flask_talisman import Talisman
from frontend.assets import compile_static_assets
from fsd_utils.logging import logging
from jinja2 import ChoiceLoader
from jinja2 import PackageLoader
from jinja2 import PrefixLoader
from openapi.utils import get_bundled_specs


def create_app() -> Flask:

    # Configure Connexion and Swagger
    connexion_options = {
        "swagger_url": "/docs",
        "swagger_ui_template_arguments": {},
    }

    connexion_app = connexion.FlaskApp(
        "Template Repo",
        specification_dir="/openapi/",
        options=connexion_options,
    )

    connexion_app.add_api(
        get_bundled_specs("/openapi/api.yml"),
        validate_responses=True,
        resolver=MethodViewResolver("api"),
    )

    # Configure flask_app
    flask_app = connexion_app.app
    flask_app.config.from_object("config.Config")

    # Configure jinja templates and static files
    flask_app.static_url_path = flask_app.config.get("STATIC_URL_PATH")
    flask_app.static_folder = flask_app.config.get("STATIC_FOLDER")

    flask_app.jinja_loader = ChoiceLoader(
        [
            PackageLoader("frontend"),
            PrefixLoader(
                {"govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja")}
            ),
        ]
    )

    flask_app.jinja_env.trim_blocks = True
    flask_app.jinja_env.lstrip_blocks = True

    # Initialise logging
    logging.init_app(flask_app)

    # TODO : Uncomment and setup redis if using redis sessions
    # Initialise redis sessions
    # session = Session()
    # session.init_app(flask_app)

    # Configure application security with Talisman
    talisman = Talisman(flask_app, **Config.TALISMAN_SETTINGS)

    # This section is needed for url_for("foo", _external=True) to
    # automatically generate http scheme when this sample is
    # running on localhost, and to generate https scheme when it is
    # deployed behind reversed proxy.
    # See also #proxy_setups section at
    # flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone
    from werkzeug.middleware.proxy_fix import ProxyFix

    flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_proto=1, x_host=1)

    # Disable strict talisman on swagger docs pages
    @flask_app.before_request
    def before_request_modifier():
        if request.path.startswith("/docs"):
            talisman.content_security_policy = Config.SWAGGER_CSP
        else:
            talisman.content_security_policy = Config.SECURE_CSP
            talisman.content_security_policy_nonce_in = ["script-src"]

    # This is silently used by flask in the background.
    @flask_app.context_processor
    def inject_global_constants():
        return dict(
            stage="beta",
            service_title="Funding Service Design - TEMPLATE",
            service_meta_description=(
                "Funding Service Design Iteration - TEMPLATE"
            ),
            service_meta_keywords="Funding Service Design - TEMPLATE",
            service_meta_author="DLUHC",
        )

    with flask_app.app_context():
        from frontend.default.routes import (
            default_bp,
            not_found,
            internal_server_error,
        )

        flask_app.register_error_handler(404, not_found)
        flask_app.register_error_handler(500, internal_server_error)
        flask_app.register_blueprint(default_bp)

        # Bundle and compile assets
        assets = Environment()
        assets.init_app(flask_app)
        compile_static_assets(assets, flask_app)

        # Setup database
        from db import db, migrate

        # Bind SQLAlchemy ORM to Flask app
        db.init_app(flask_app)
        # Bind Flask-Migrate db utilities to Flask app
        migrate.init_app(flask_app, db, directory="db/migrations")

        return flask_app


app = create_app()
