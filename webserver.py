import json
import os
from pathlib import Path

from flask import Flask, render_template, request

from desk import Desk
from utils import conf

app = Flask(__name__)

desk_conf = conf["segments"]
if "TEST_SEGMENTS" in os.environ:
    desk_conf = json.loads(os.environ["TEST_SEGMENTS"])

app.desk = Desk(desk_conf)
app.segments = app.desk.segments


@app.route("/", methods=["GET"])
def index():
    """Root endpoint."""
    if request.accept_mimetypes["text/html"]:
        return render_template("index.html", title="RGB Desk", segments=app.segments)

    return {"status": "OK"}


@app.route("/desk/segments/<segment_name>/sweep", methods=["POST"])
def sweep_segment(segment_name):
    """Sweep a colour across a segment."""
    if not request.content_length:
        return {"error": "no data"}, 422

    if segment_name not in app.segments:
        return {"error": "no such segment"}, 404

    app.data = validate_sweep(request.get_json())

    if "invalid" in app.data:
        return {"error": app.data["invalid"]}, 422

    colour = app.data["colour"]
    delay = app.data["delay"]
    direction = app.data["direction"]
    segment = app.desk.segments[segment_name]
    segment.sweep(colour, delay=delay, direction=direction)

    Path("data/segments").mkdir(parents=True, exist_ok=True)
    Path("data/segments", segment_name).write_text(json.dumps(colour))
    return {"colour": colour, "status": "OK"}


@app.route("/desk/all/sweep", methods=["POST"])
def sweep_all():
    """Sweep a colour across the whole desk."""
    if not request.content_length:
        return {"error": "no data"}, 422

    app.data = validate_sweep(request.get_json())

    if "invalid" in app.data:
        return {"error": app.data["invalid"]}, 422

    colour = app.data["colour"]
    delay = app.data["delay"]
    direction = app.data["direction"]
    app.desk.sweep(colour, delay=delay, direction=direction)

    Path("data/").mkdir(parents=True, exist_ok=True)
    Path("data/desk").write_text(json.dumps(colour))
    return {"colour": colour, "status": "OK"}


@app.route("/desk/segments/<segment_name>", methods=["GET"])
def current_segment_colour(segment_name):
    """Return the segment's colour."""
    try:
        colour = Path("data/segments", segment_name).read_text()
        return {"colour": json.loads(colour), "status": "OK"}

    except FileNotFoundError:
        return {"error": "no data about that segment"}, 404


@app.route("/desk/all", methods=["GET"])
def current_desk_colour():
    """Return the desk's colour."""
    try:
        colour = Path("data/desk").read_text()
        return {"colour": json.loads(colour), "status": "OK"}

    except FileNotFoundError:
        return {"error": "no data for that"}, 404


# validators


def validate_sweep(data):
    """Validate the data for a `sweep`."""
    if "colour" not in data:
        data["invalid"] = "`colour` must be supplied"
        return data

    colour = data["colour"]
    invalid = invalid_colour(colour)
    if invalid:
        data["invalid"] = invalid
        return data

    try:
        direction = data["direction"]
        invalid = invalid_direction(direction)
        if invalid:
            data["invalid"] = invalid
            return data

    except KeyError:
        data["direction"] = "forwards"

    try:
        delay = data["delay"]
        invalid = invalid_delay(delay)
        if invalid:
            data["invalid"] = invalid
            return data

    except KeyError:
        data["delay"] = 0.01

    return data


def invalid_direction(direction):
    """Validate the `direction` parameter."""
    valid_directions = ["forwards", "backwards"]

    if direction not in valid_directions:
        return f"`direction` must be one of [{', '.join(valid_directions)}]"

    return False


def invalid_colour(colour):
    """Validate the RGB colour."""
    error_message = f"`{colour}` is not a valid RGB colour"

    if not isinstance(colour, list):
        return error_message

    if not all([0 <= component <= 255 for component in colour]):
        return error_message

    return False


def invalid_delay(delay):
    """Validate the interval."""
    try:
        int(delay)
    except ValueError:
        return f"`{delay}` is not a valid delay interval"


if __name__ == "__main__":  # nocov
    app.run(host="0.0.0.0", debug=True)
