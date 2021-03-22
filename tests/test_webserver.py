import json
import os
from unittest.mock import patch

with patch.dict(os.environ, {"TEST_SEGMENTS": json.dumps({"foo": [[0, 1]]})}):
    from webserver import app


def test_root():
    """Test '/'."""
    client = app.test_client()
    response = client.get("/", headers={"Accept": "application/json"})
    assert response.get_json() == {"status": "OK"}


def test_root_html():
    """Test '/'."""
    client = app.test_client()
    response = client.get("/", headers={"Accept": "text/html"})
    assert response.data.decode().split("\n")[0] == "<!DOCTYPE HTML>"
