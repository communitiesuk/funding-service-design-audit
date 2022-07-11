import pytest
from app import create_app
from tests.mocks.redis_sessions import RedisSessions
from tests.mocks.sqlite_test_db import SqliteTestDB


@pytest.fixture(scope="session")
def app(session_mocker):
    """
    Returns an instance of the Flask app as a fixture for testing,
    which is available for the testing session and accessed with the
    @pytest.mark.uses_fixture('live_server')
    :return: An instance of the Flask app.
    """

    session_mocker.patch("redis.Redis.get", RedisSessions.get)
    session_mocker.patch("redis.Redis.set", RedisSessions.set)
    session_mocker.patch("redis.Redis.delete", RedisSessions.delete)
    session_mocker.patch("redis.Redis.setex", RedisSessions.setex)
    with create_app().app_context():
        SqliteTestDB.create()
        yield create_app()
        SqliteTestDB.remove()
