import json
import os
from unittest import TestCase
from unittest.mock import MagicMock, patch

with patch.dict(os.environ, {"TEST_SEGMENTS": json.dumps({"foo": [[0, 1]]})}):
    from webserver import app

headers = {"Accept": "application/json", "Content-type": "application/json"}


class TestSweepSegment(TestCase):
    """Test `sweep` across a segment."""

    def test_easy_sweep(self):
        """Test the simple case."""
        client = app.test_client()
        app.desk.segments["foo"] = MagicMock()
        data = json.dumps({"colour": [123, 123, 0]})
        response = client.post("/desk/segments/foo/sweep", headers=headers, data=data)

        app.desk.segments["foo"].sweep.assert_called_with(
            [123, 123, 0], delay=0.01, direction="forwards"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data), {"colour": [123, 123, 0], "status": "OK"}
        )

    def test_with_parameters(self):
        """Test with params."""
        client = app.test_client()
        app.desk.segments["foo"] = MagicMock()
        data = json.dumps(
            {"colour": [10, 20, 30], "direction": "backwards", "delay": 0.1}
        )
        response = client.post("/desk/segments/foo/sweep", headers=headers, data=data)

        app.desk.segments["foo"].sweep.assert_called_with(
            [10, 20, 30], delay=0.1, direction="backwards"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data), {"colour": [10, 20, 30], "status": "OK"}
        )

    def test_with_bad_segment(self):
        """Test it complains about a duff segment."""
        client = app.test_client()
        data = json.dumps({"colour": [123, 123, 0]})
        response = client.post("/desk/segments/bar/sweep", headers=headers, data=data)

        self.assertEqual(response.status_code, 404)

    #     # self.assertEqual(
    #     #     json.loads(response.data),
    #     #     {"error": "no data"},
    #     # )

    def test_with_no_data(self):
        """Test it rejects an empty payload."""
        client = app.test_client()
        data = None
        response = client.post("/desk/segments/foo/sweep", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "no data"},
        )

    def test_with_bad_colour(self):
        """Test it rejects a bogus colour."""
        client = app.test_client()
        data = json.dumps({"colour": [400, -35, 127]})
        response = client.post("/desk/segments/foo/sweep", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "`[400, -35, 127]` is not a valid RGB colour"},
        )

    def test_with_really_bad_colour(self):
        """Test it rejects a totally bogus colour."""
        client = app.test_client()
        data = json.dumps({"colour": "mauve"})
        response = client.post("/desk/segments/foo/sweep", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "`mauve` is not a valid RGB colour"},
        )

    def test_with_no_colour(self):
        """Test it rejects a payload with no colour."""
        client = app.test_client()
        data = json.dumps({})
        response = client.post("/desk/segments/foo/sweep", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "`colour` must be supplied"},
        )

    def test_with_bad_direction(self):
        """Test it rejects a bogus `direction` parameter."""
        client = app.test_client()
        data = json.dumps({"colour": [10, 20, 30], "direction": "up"})
        response = client.post("/desk/segments/foo/sweep", headers=headers, data=data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "`direction` must be one of [forwards, backwards]"},
        )

    def test_with_bad_delay(self):
        """Test it rejects a bogus `delay` parameter."""
        client = app.test_client()
        data = json.dumps({"colour": [10, 20, 30], "delay": "two days"})
        response = client.post("/desk/segments/foo/sweep", headers=headers, data=data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json.loads(response.data),
            {"error": "`two days` is not a valid delay interval"},
        )

    def test_get_colour(self):
        """Test it records and returns the colour."""
        client = app.test_client()
        data = json.dumps({"colour": [12, 34, 56]})
        client.post("/desk/segments/foo/sweep", headers=headers, data=data)
        response = client.get("/desk/segments/foo")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data),
            {"colour": [12, 34, 56], "status": "OK"},
        )

    def test_get_no_colour(self):
        """Test it's OK when there's no colour recorded."""
        if os.path.exists("data/segments/foo"):
            os.remove("data/segments/foo")

        client = app.test_client()
        response = client.get("/desk/segments/foo")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            json.loads(response.data),
            {"error": "no data about that segment"},
        )
