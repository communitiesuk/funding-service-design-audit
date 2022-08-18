class TestHealthchecks:
    def test_healthcheck(self, flask_test_client):
        result = flask_test_client.get("/healthcheck")
        expected_dict = {
            "checks": [{"check_flask_running": "OK"}, {"check_db": "OK"}]
        }
        assert 200 == result.status_code, "unexpected response code"
        assert expected_dict == result.json, "unexpected json response"
