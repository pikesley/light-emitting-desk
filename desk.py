import re
from collections import OrderedDict

import light_modes
# from light_modes import Converger, SectorDiverger, SpotFiller, Sweeper
from segment import Segment
from utils import get_neopixels


class Desk:
    """Class representing a NeoPixelled desk."""

    def __init__(self, segment_data):
        """Construct."""
        self.pixels = get_neopixels(segment_data)
        self.segments = OrderedDict()
        self.sectors = []

        for name, limits in segment_data.items():
            self.segments[name] = Segment(name, limits, self)

            for pair in limits:
                start, end = pair
                if start > end:
                    end, start = pair
                self.sectors.append(list(range(start, end + 1)))

        self.sectors.sort()

        self.indeces = []
        for _, segment in self.segments.items():
            self.indeces.extend(segment.indeces)

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
    return getattr(light_modes, to_camel_case(name))


def to_camel_case(snake_case):
    """Turn `snake_case_name` or `slug-name` into `CamelCaseName`."""
    name = ""
    for word in re.split(r"[-_]", snake_case):
        name += word.title()

    return name


# def pairs_from_list(lights):
#     """Generate a list of pairs to enable from-each-end lighting."""
#     length = len(lights)
#     half = int(length / 2)
#     offset = 0

#     centre = None
#     if length % 2 == 1:
#         centre = lights[half]
#         offset = 1

#     left = lights[:half]

#     rh_start = half + offset
#     right = reversed(lights[rh_start:])

#     pairs = list(map(list, zip(left, right)))

#     if centre:
#         pairs.append([centre])

#     return pairs


# def divergence_sequence_for_sectors(sectors):
#     """Generate a sequence for divergent lighting per-sector."""
#     sequence = []
#     pairs = map(pairs_from_list, sectors)
#     for items in pairs:
#         for j, pair in enumerate(reversed(items)):
#             try:
#                 sequence[j].extend(pair)
#             except IndexError:
#                 sequence.append(pair)

#     # sort the member lists
#     return list(map(sorted, sequence))
