"""Flask Test Environment Configuration."""
import logging
from os import environ

from config.envs.default import DefaultConfig as Config
from fsd_utils import configclass


@configclass
class TestConfig(Config):

    SECRET_KEY = environ.get("SECRET_KEY", "test")

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG