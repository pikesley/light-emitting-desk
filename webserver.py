import json
import os

import redis
from flask import Flask, render_template, request

from light_emitting_desk.desk import Desk
from light_emitting_desk.utils import conf

app = Flask(__name__)
app.redis = redis.Redis()

desk_conf = conf["sectors"]
if "TEST_SECTORS" in os.environ:
    desk_conf = json.loads(os.environ["TEST_SECTORS"])

app.desk = Desk(desk_conf)

mode_names = list(map(lambda x: x["name"], conf["modes"]))


@app.route("/", methods=["GET"])
def index():
    """Root endpoint."""
    if request.accept_mimetypes["text/html"]:
        return render_template(
            "index.html",
            title="LED",
            imports=conf["web"]["imports"],
            modes=conf["modes"],
        )

    return {"status": "OK"}


@app.route("/desk/light", methods=["POST"])
def set_colour():
    """Light the desk."""
    app.data = validate_request(request)

    if "invalid" in app.data:
        return {"error": app.data["invalid"]}, 422

    return enqueue_and_return(app.data)


@app.route("/desk/off", methods=["POST"])
def switch_off():
    """Instantly turn it all off."""
    app.redis.flushall()
    colour = [0, 0, 0]
    app.data = {"colour": colour, "mode": "sector-diverge"}
    return enqueue_and_return(app.data)


@app.route("/desk/colour", methods=["GET"])
def current_desk_colour():
    """Return the desk's colour."""
    try:
        colour = json.loads(app.redis.get("colours/desk"))
        return {"colour": colour, "status": "OK"}

    except TypeError:
        return {"error": "no data for that"}, 404


def enqueue_and_return(data):
    """Light the lights."""
    app.redis.rpush("jobs", json.dumps(data))

    app.redis.set("colours/desk", json.dumps(data["colour"]))
    return {"colour": data["colour"], "status": "OK"}


# validators


def validate_request(req):
    """Validate the request data."""
    mandatory_fields = conf["api"]["mandatory-fields"]
    optional_fields = conf["api"]["optional-fields"]

    if not req.content_length:
        return {"invalid": "no data"}

    data = req.get_json()

    for field in mandatory_fields:
        if field not in data:
            data["invalid"] = f"`{field}` must be supplied"
            return data

        invalid = globals()[f"invalid_{field}"](data[field])
        if invalid:
            data["invalid"] = invalid
            return data

    for field, default in optional_fields.items():
        try:
            invalid = globals()[f"invalid_{field.replace('-', '_')}"](data[field])
            if invalid:
                data["invalid"] = invalid
                return data

        except KeyError:
            data[field] = default

    return data


def invalid_colour(colour):
    """Validate the RGB colour."""
    error_message = f"`{colour}` is not a valid RGB colour"

    if not isinstance(colour, list):
        return error_message

    if not all([0 <= component <= 255 for component in colour]):
        return error_message

    return False


def invalid_mode(mode):
    """Validate the mode."""
    valid_modes = list(map(lambda x: x["name"], conf["modes"]))

    if mode not in valid_modes:
        return f"`{mode}` is not a recognised mode"

    return False


def invalid_delay(delay):
    """Validate the interval."""
    try:
        int(delay)
    except ValueError:
        return f"`{delay}` is not a valid delay interval"


def invalid_direction(direction):
    """Validate the `direction` parameter."""
    valid_directions = ["forwards", "backwards"]

    if direction not in valid_directions:
        return f"`direction` must be one of [{', '.join(valid_directions)}]"

    return False


def invalid_caterpillar_length(length):
    """Validate the `caterpillar-length` parameter."""
    try:
        length = int(length)
    except ValueError:
        return "`caterpillar-length` must be something that can be cast to an `int`"

    if not 1 <= length <= len(app.desk.indeces):
        return (
            "`caterpillar-length` must be a number between "
            f"1 and {len(app.desk.indeces)}"
        )

    return False


if __name__ == "__main__":  # nocov
    app.run(host="0.0.0.0", debug=True)
