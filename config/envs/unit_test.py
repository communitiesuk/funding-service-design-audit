"""Flask Local Development Environment Configuration."""
import logging
from os import path

from config.envs.default import DefaultConfig as Config
from fsd_utils import configclass


@configclass
class UnitTestConfig(Config):
    #  Application Config
    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = "session_cookie"

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG

    SESSION_TYPE = (
        # Specifies how the token cache should be stored
        # in server-side session
        # "filesystem"
        "redis"
    )
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True

    # External Services
    USE_LOCAL_DATA = True

    # RSA 256 KEYS
    _test_private_key_path = (
        Config.FLASK_ROOT + "/tests/keys/rsa256/private.pem"
    )
    with open(_test_private_key_path, mode="rb") as private_key_file:
        RSA256_PRIVATE_KEY = private_key_file.read()
    _test_public_key_path = Config.FLASK_ROOT + "/tests/keys/rsa256/public.pem"
    with open(_test_public_key_path, mode="rb") as public_key_file:
        RSA256_PUBLIC_KEY = public_key_file.read()

    # Security
    FORCE_HTTPS = False

    # Database
    SQLITE_DB_NAME = "test_sqlite.db"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(
        Config.FLASK_ROOT, SQLITE_DB_NAME
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
