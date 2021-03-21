import json
from pathlib import Path

from flask import Flask, render_template, request

from desk import Desk
from utils import conf

app = Flask(__name__)
app.desk = Desk()
app.segments = conf["segments"]


@app.route("/", methods=["GET"])
def index():
    """Root endpoint."""
    if request.accept_mimetypes["text/html"]:
        return render_template("index.html", title="RGB Desk", segments=app.segments)

    return {"status": "OK"}


@app.route("/desk/segments/<segment_name>/sweep", methods=["POST"])
def sweep(segment_name):
    """Sweep a colour."""
    if not request.content_length:
        return {"error": "No data"}, 422

    app.data = request.get_json()
    if "colour" not in app.data:
        return {"error": "`colour` must be supplied"}, 422

    colour = app.data["colour"]

    try:
        direction = app.data["direction"]

    except KeyError:
        direction = "forwards"

    try:
        delay = app.data["delay"]

    except KeyError:
        delay = 0.01

    try:
        segment = app.desk.segments[segment_name]
        segment.sweep(colour, delay=delay, direction=direction)

    except KeyError:
        return {"error": "No such segment"}, 422

    Path("data/segments").mkdir(parents=True, exist_ok=True)
    Path("data/segments", segment_name).write_text(json.dumps(colour))
    return {"colour": colour, "status": "OK"}

@app.route("/desk/segments/<segment_name>/from-random", methods=["POST"])
def settle_from_random(segment_name):
    """Sweep a colour."""
    if not request.content_length:
        return {"error": "No data"}, 422

    app.data = request.get_json()
    if "colour" not in app.data:
        return {"error": "`colour` must be supplied"}, 422

    colour = app.data["colour"]

    try:
        direction = app.data["direction"]

    except KeyError:
        direction = "forwards"

    try:
        steps = app.data["steps"]

    except KeyError:
        steps = 16

    try:
        delay = app.data["delay"]

    except KeyError:
        delay = 0.01

    try:
        segment = app.desk.segments[segment_name]
        segment.settle_from_random(colour, steps=steps,delay=delay)

    except KeyError:
        return {"error": "No such segment"}, 422

    Path("data/segments").mkdir(parents=True, exist_ok=True)
    Path("data/segments", segment_name).write_text(json.dumps(colour))
    return {"colour": colour, "status": "OK"}

@app.route("/desk/segments/<segment_name>", methods=["GET"])
def current_colour(segment_name):
    """Return the segment's colour."""
    try:
        colour = Path("data/segments", segment_name).read_text()
        return {"colour": json.loads(colour), "status": "OK"}

    except FileNotFoundError:
        return {"error": "No data about that segment"}, 422


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
