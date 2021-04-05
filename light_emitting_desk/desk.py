import re

import light_emitting_desk.light_modes
from light_emitting_desk.utils import get_neopixels


class Desk:
    """Class representing a NeoPixelled desk."""

    def __init__(self, sector_data):
        """Construct."""
        self.pixels = get_neopixels(sector_data)

        self.sectors = []
        self.indeces = []

        for _, limits in sector_data.items():
            for pair in limits:
                start, end = pair
                step = offset = 1
                if start > end:
                    step = offset = -1

                sector = list(range(start, end + offset, step))
                self.sectors.append(sector)
                self.indeces.extend(sector)

    def __setitem__(self, index, colour):
        """Override `x[i] = 'foo'`."""
        self.pixels[index] = colour

    def __getitem__(self, index):
        """Override `x[i]`."""
        return self.pixels[index]

    def fill(self, colour):
        """Fill our pixels with a colour."""
        self.pixels.fill(colour)
        self.show()

    def show(self):
        """`show` the pixels."""
        self.pixels.show()

    def light_up(self, colour, args):
        """Call a LightMode."""
        actual_class = get_class(args["mode"])
        mode = actual_class(self, colour, args)
        mode.run()


def get_class(name):
    """Turn a string into a ClassName."""
    return getattr(light_emitting_desk.light_modes, to_camel_case(name))


def to_camel_case(snake_case):
    """Turn `snake_case_name` or `slug-name` into `CamelCaseName`."""
    name = ""
    for word in re.split(r"[-_]", snake_case):
        name += word.title()

    return name
