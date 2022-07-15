import connexion
from config import Config
from connexion.resolver import MethodViewResolver
from flask import Flask
from flask import request
from flask_talisman import Talisman
from fsd_utils.logging import logging
from openapi.utils import get_bundled_specs
from sqlalchemy import event

def create_app() -> Flask:

    # Configure Connexion and Swagger
    connexion_options = {
        "swagger_url": "/docs",
        "swagger_ui_template_arguments": {},
    }

    connexion_app = connexion.FlaskApp(
        "Audit Service",
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

    # Initialise logging
    logging.init_app(flask_app)

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

    # Ensure FOREIGN KEY for sqlite3
    if 'sqlite' in flask_app.config['SQLALCHEMY_DATABASE_URI']:
        def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
            dbapi_con.execute('pragma foreign_keys=ON')

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

    # For circular imports
    with flask_app.app_context():
        # Setup database
        from db import db, migrate

        # Bind SQLAlchemy ORM to Flask app
        db.init_app(flask_app)
        # Bind Flask-Migrate db utilities to Flask app
        migrate.init_app(flask_app, db, directory="db/migrations")

        # Turn on FK enforce when using SQLite
        event.listen(db.engine, 'connect', _fk_pragma_on_connect)

        return flask_app

app = create_app()
