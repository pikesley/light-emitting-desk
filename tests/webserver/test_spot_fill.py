import json
import os
from unittest import TestCase
from unittest.mock import MagicMock, patch

import redis

with patch.dict(
    os.environ, {"TEST_SEGMENTS": json.dumps({"foo": [[0, 3]], "bar": [[4, 7]]})}
):
    from webserver import app
    from worker import Worker

headers = {"Accept": "application/json", "Content-type": "application/json"}
redis = redis.Redis()
worker = Worker()
worker.desk.light_up = MagicMock()


class TestSpotFill(TestCase):
    """Test `spot-fill`."""

    def setUp(self):
        """Do some initialisation."""
        redis.flushall()

    def test_easy_spot(self):
        """Test the simple case."""
        client = app.test_client()
        data = json.dumps({"colour": [123, 123, 0]})
        response = client.post("/desk/all/spot-fill", headers=headers, data=data)

        worker.poll()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data), {"colour": [123, 123, 0], "status": "OK"}
        )

    def test_with_parameters(self):
        """Test with params."""
        client = app.test_client()
        data = json.dumps({"colour": [10, 20, 30], "delay": 0.1})
        response = client.post("/desk/all/spot-fill", headers=headers, data=data)

        worker.poll()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data), {"colour": [10, 20, 30], "status": "OK"}
        )

    def test_with_no_data(self):
        """Test it rejects an empty payload."""
        client = app.test_client()
        data = None
        response = client.post("/desk/all/spot-fill", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "no data"},
        )

    def test_get_mode(self):
        """Test it records and returns the mode."""
        client = app.test_client()
        data = json.dumps({"colour": [12, 34, 56]})
        client.post("/desk/all/spot-fill", headers=headers, data=data)
        response = client.get("/desk/mode")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data),
            {"mode": "spot-fill", "status": "OK"},
        )

    def test_get_no_mode(self):
        """Test it's OK when there's no mode recorded."""
        app.redis.delete("mode")

        client = app.test_client()
        response = client.get("/desk/mode")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            json.loads(response.data),
            {"error": "no data for that"},
        )
