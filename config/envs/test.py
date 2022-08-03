"""Flask Test Environment Configuration."""
import logging
from os import environ

from config.envs.default import DefaultConfig
from fsd_utils import configclass


@configclass
class TestConfig(DefaultConfig):

    SECRET_KEY = environ.get("SECRET_KEY", "test")

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL").replace(
        "postgres://", "postgresql://"
    )
