from collections import OrderedDict

from segment import Segment
from utils import get_neopixels


class Desk:
    """Class representing a NeoPixelled desk."""

    def __init__(self, segment_data):
        """Construct."""
        self.pixels = get_neopixels()
        self.segments = OrderedDict()

        for name, limits in segment_data.items():
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

    def sweep(self, colour, direction="forwards", delay=0.01):
        """Sweep across the whole desk."""
        keys = self.segments.keys()
        if direction == "backwards":
            keys = reversed(keys)

        for key in keys:
            self.segments[key].sweep(colour, direction=direction, delay=delay)
