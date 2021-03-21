from segment import Segment
from utils import conf, get_neopixels


class Desk:
    """Class representing a NeoPixelled desk."""

    def __init__(self):
        """Construct."""
        self.pixels = get_neopixels()
        self.segments = {}
        for name, limits in conf["segments"].items():
            self.segments[name] = Segment(name, limits, self)

    def __setitem__(self, index, colour):
        """Override `x[i] = 'foo'`."""
        self.pixels[index] = colour

    def __getitem__(self, index):
        """Override `x[i]`."""
        return self.pixels[index]

    def show(self):
        """`show` the pixels."""
        self.pixels.show()
