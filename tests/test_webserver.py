import json
import os
from unittest import TestCase
from unittest.mock import patch

with patch.dict(os.environ, {"TEST_SECTORS": json.dumps({"foo": [[0, 1]]})}):
    from webserver import app

headers = {"Accept": "application/json", "Content-type": "application/json"}


class TestWebserver(TestCase):
    """Test the webserver."""

    def test_root(self):
        """Test '/'."""
        client = app.test_client()
        response = client.get("/", headers=headers)
        self.assertEqual(response.get_json(), {"status": "OK"})

    def test_root_html(self):
        """Test '/'."""
        client = app.test_client()
        response = client.get("/", headers={"Accept": "text/html"})
        self.assertEqual(response.data.decode().split("\n")[0], "<!DOCTYPE HTML>")

    def test_with_no_data(self):
        """Test it rejects an empty payload."""
        client = app.test_client()
        data = None
        response = client.post(
            "/desk/light",
            headers=headers,
            data=data,
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(json.loads(response.data), {"error": "no data"})

    def test_bad_mode(self):
        """Test it rejects an unknown mode."""
        client = app.test_client()
        response = client.post(
            "/desk/light",
            headers=headers,
            data=json.dumps({"colour": [123, 123, 0], "mode": "phony-mode"}),
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.get_json(), {"error": "`phony-mode` is not a recognised mode"}
        )

    def test_no_mode(self):
        """Test it rejects a payload with no mode."""
        client = app.test_client()
        response = client.post(
            "/desk/light",
            headers=headers,
            data=json.dumps({"colour": [123, 123, 0]}),
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.get_json(), {"error": "`mode` must be supplied"})

    def test_with_bad_colour(self):
        """Test it rejects a bogus colour."""
        client = app.test_client()
        data = json.dumps({"colour": [400, -35, 127], "mode": "sweep"})
        response = client.post("/desk/light", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "`[400, -35, 127]` is not a valid RGB colour"},
        )

    def test_with_really_bad_colour(self):
        """Test it rejects a totally bogus colour."""
        client = app.test_client()
        data = json.dumps({"colour": "mauve", "mode": "sweep"})
        response = client.post("/desk/light", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "`mauve` is not a valid RGB colour"},
        )

    def test_with_no_colour(self):
        """Test it rejects a payload with no colour."""
        client = app.test_client()
        data = json.dumps({})
        response = client.post("/desk/light", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "`colour` must be supplied"},
        )

    def test_with_bad_direction(self):
        """Test it rejects a bogus `direction` parameter."""
        client = app.test_client()
        data = json.dumps({"colour": [10, 20, 30], "mode": "sweep", "direction": "up"})
        response = client.post("/desk/light", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "`direction` must be one of [forwards, backwards]"},
        )

    def test_with_bad_delay(self):
        """Test it rejects a bogus `delay` parameter."""
        client = app.test_client()
        data = json.dumps(
            {"colour": [10, 20, 30], "mode": "sweep", "delay": "two days"}
        )
        response = client.post("/desk/light", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "`two days` is not a valid delay interval"},
        )

    def test_with_non_number_caterpillar_length(self):
        """Test it rejects a non-numeric `caterpillar-length` parameter."""
        client = app.test_client()
        data = json.dumps(
            {
                "colour": [10, 20, 30],
                "mode": "caterpillar",
                "caterpillar-length": "seven",
            }
        )
        response = client.post("/desk/light", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {
                "error": (
                    "`caterpillar-length` must be something "
                    "that can be cast to an `int`"
                )
            },
        )

    def test_with_out_of_range_caterpillar_length(self):
        """Test it rejects an out-of-range `caterpillar-length` parameter."""
        client = app.test_client()
        data = json.dumps(
            {
                "colour": [10, 20, 30],
                "mode": "caterpillar",
                "caterpillar-length": 21,
            }
        )
        response = client.post("/desk/light", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": ("`caterpillar-length` must be a number between 1 and 2")},
        )

    def test_get_colour(self):
        """Test it records and returns the colour."""
        client = app.test_client()
        data = json.dumps({"colour": [12, 34, 56], "mode": "sweep"})
        client.post("/desk/light", headers=headers, data=data)
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
