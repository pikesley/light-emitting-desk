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


def test_bad_mode():
    """Test we get a 404 for an unknown mode."""
    client = app.test_client()
    response = client.post(
        "/desk/all/phony-mode", headers={"Accept": "application/json"}
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "`phony-mode` is not a recognised mode"}
