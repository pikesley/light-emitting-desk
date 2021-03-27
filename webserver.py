import json
import os

import redis
from flask import Flask, render_template, request

from rgb_desk.desk import Desk
from rgb_desk.utils import conf

app = Flask(__name__)
app.redis = redis.Redis()

desk_conf = conf["segments"]
if "TEST_SEGMENTS" in os.environ:
    desk_conf = json.loads(os.environ["TEST_SEGMENTS"])

app.desk = Desk(desk_conf)
app.segments = app.desk.segments
app.mode_names = list(map(lambda x: x["name"], conf["modes"]))


@app.route("/", methods=["GET"])
def index():
    """Root endpoint."""
    if request.accept_mimetypes["text/html"]:
        return render_template("index.html", title="RGB Desk", modes=conf["modes"])

    return {"status": "OK"}


@app.route("/desk/all/<mode>", methods=["POST"])
def light_desk(mode):
    """Light the desk using `mode`."""
    if mode not in app.mode_names:
        return {"error": f"`{mode}` is not a recognised mode"}, 404

    app.data = validate_request(request)

    if "invalid" in app.data:
        return {"error": app.data["invalid"]}, 422

    app.data["mode"] = mode
    app.redis.rpush("jobs", json.dumps(app.data))

    app.redis.set("colours/desk", json.dumps(app.data["colour"]))
    app.redis.set("mode", mode)
    return {"colour": app.data["colour"], "status": "OK"}


@app.route("/desk/colour", methods=["GET"])
def current_desk_colour():
    """Return the desk's colour."""
    try:
        colour = json.loads(app.redis.get("colours/desk"))
        return {"colour": colour, "status": "OK"}

    except TypeError:
        return {"error": "no data for that"}, 404


@app.route("/desk/mode", methods=["GET"])
def current_mode():
    """Return the current mode."""
    try:
        mode = app.redis.get("mode").decode()
        return {"mode": mode, "status": "OK"}

    except AttributeError:
        return {"error": "no data for that"}, 404


# validators


def validate_request(req):
    """Validate the data for a `sweep`."""
    if not req.content_length:
        return {"invalid": "no data"}

    data = req.get_json()

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


# @app.route("/desk/segments/<segment_name>/sweep", methods=["POST"])
# def sweep_segment(segment_name):
#     """Sweep a colour across a segment."""
#     if segment_name not in app.segments:
#         return {"error": f"no such segment `{segment_name}`"}, 404

#     app.data = validate_request(request)

#     if "invalid" in app.data:
#         return {"error": app.data["invalid"]}, 422

#     app.data["target"] = segment_name
#     app.data["method"] = "sweep"
#     app.redis.rpush("jobs", json.dumps(app.data))

#     app.redis.set(f"colours/segments/{segment_name}", json.dumps(app.data["colour"]))
#     return {"colour": app.data["colour"], "status": "OK"}

# @app.route("/desk/segments/<segment_name>", methods=["GET"])
# def current_segment_colour(segment_name):
#     """Return the segment's colour."""
#     try:
#         colour = json.loads(app.redis.get(f"colours/segments/{segment_name}"))
#         return {"colour": colour, "status": "OK"}

#     except TypeError:
#         return {"error": "no data about that segment"}, 404
