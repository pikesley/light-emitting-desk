import json
import os
from unittest import TestCase
from unittest.mock import MagicMock, patch

import redis

with patch.dict(os.environ, {"TEST_SEGMENTS": json.dumps({"foo": [[0, 1]]})}):
    from webserver import app
    from worker import Worker

headers = {"Accept": "application/json", "Content-type": "application/json"}
redis = redis.Redis()
worker = Worker()
worker.desk.light_up = MagicMock()


class TestSweep(TestCase):
    """Test `sweep` across the whole desk."""

    def setUp(self):
        """Do some initialisation."""
        redis.flushall()

    def test_easy_sweep(self):
        """Test the simple case."""
        client = app.test_client()
        data = json.dumps({"colour": [123, 123, 0]})
        response = client.post("/desk/all/sweep", headers=headers, data=data)

        worker.poll()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data), {"colour": [123, 123, 0], "status": "OK"}
        )

    def test_with_parameters(self):
        """Test with params."""
        client = app.test_client()
        data = json.dumps(
            {"colour": [10, 20, 30], "direction": "backwards", "delay": 0.1}
        )
        response = client.post("/desk/all/sweep", headers=headers, data=data)

        worker.poll()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data), {"colour": [10, 20, 30], "status": "OK"}
        )

    def test_with_no_data(self):
        """Test it rejects an empty payload."""
        client = app.test_client()
        data = None
        response = client.post("/desk/all/sweep", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "no data"},
        )

    def test_with_bad_colour(self):
        """Test it rejects a bogus colour."""
        client = app.test_client()
        data = json.dumps({"colour": [400, -35, 127]})
        response = client.post("/desk/all/sweep", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "`[400, -35, 127]` is not a valid RGB colour"},
        )

    def test_with_really_bad_colour(self):
        """Test it rejects a totally bogus colour."""
        client = app.test_client()
        data = json.dumps({"colour": "mauve"})
        response = client.post("/desk/all/sweep", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "`mauve` is not a valid RGB colour"},
        )

    def test_with_no_colour(self):
        """Test it rejects a payload with no colour."""
        client = app.test_client()
        data = json.dumps({})
        response = client.post("/desk/all/sweep", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "`colour` must be supplied"},
        )

    def test_with_bad_direction(self):
        """Test it rejects a bogus `direction` parameter."""
        client = app.test_client()
        data = json.dumps({"colour": [10, 20, 30], "direction": "up"})
        response = client.post("/desk/all/sweep", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "`direction` must be one of [forwards, backwards]"},
        )

    def test_with_bad_delay(self):
        """Test it rejects a bogus `delay` parameter."""
        client = app.test_client()
        data = json.dumps({"colour": [10, 20, 30], "delay": "two days"})
        response = client.post("/desk/all/sweep", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "`two days` is not a valid delay interval"},
        )

    def test_get_colour(self):
        """Test it records and returns the colour."""
        client = app.test_client()
        data = json.dumps({"colour": [12, 34, 56]})
        client.post("/desk/all/sweep", headers=headers, data=data)
        response = client.get("/desk/colour")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data),
            {"colour": [12, 34, 56], "status": "OK"},
        )

    def test_get_no_colour(self):
        """Test it's OK when there's no colour recorded."""
        app.redis.delete("colours/desk")

        client = app.test_client()
        response = client.get("/desk/colour")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            json.loads(response.data),
            {"error": "no data for that"},
        )
