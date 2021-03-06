import platform
from collections import OrderedDict
from pathlib import Path
from random import randint

import yaml

if "arm" in platform.platform():  # nocov
    import board  # pylint: disable=E0401
    from neopixel import NeoPixel  # pylint: disable=E0401


conf = OrderedDict(yaml.safe_load(Path("conf/conf.yaml").read_text()))


def total_pixels(sector_data):
    """Calculate the total number of Pixels in play."""
    highest = 0
    for sector in sector_data.values():
        for limits in sector:
            for limit in limits:
                if limit > highest:
                    highest = limit

    return highest + 1


def get_neopixels(sector_data):
    """Return real or fake pixels depending on our platform."""
    if "arm" in platform.platform():
        return NeoPixel(board.D18, total_pixels(sector_data), auto_write=False)  # nocov
    else:
        return FakeDesk(total_pixels(sector_data))


def gamma_correct(colour):
    """Gamma-correct a colour."""
    return list(map(lambda x: gamma[x], colour))


def random_colour(weighting=0):
    """Get a random RGB colour."""
    return [randint(weighting, 255), randint(weighting, 255), randint(weighting, 255)]


def scale_colour(colour, factor):
    """Scale a colour."""
    scaled = []
    for component in colour:
        scaled.append(int(component * factor))
    return scaled


def reorder_sequence_to_indeces(sequence, indeces):
    """Map a sequence to some arbitrary indeces."""
    reordered = []
    for index in indeces:
        reordered.append(sequence[index])

    return reordered


class FakeDesk(list):
    """Fake Desk for testing."""

    def __init__(self, length):  # pylint: disable=W0231
        """Construct."""
        self.length = length
        for _ in range(self.length):
            self.append((0, 0, 0))

    def show(self):
        """Pretend to show the colours."""

    def fill(self, colour):
        """Pretend to fill the pixels."""
        for i in range(self.length):
            self[i] = colour


gamma = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    3,
    3,
    3,
    3,
    3,
    3,
    3,
    4,
    4,
    4,
    4,
    4,
    5,
    5,
    5,
    5,
    6,
    6,
    6,
    6,
    7,
    7,
    7,
    7,
    8,
    8,
    8,
    9,
    9,
    9,
    10,
    10,
    10,
    11,
    11,
    11,
    12,
    12,
    13,
    13,
    13,
    14,
    14,
    15,
    15,
    16,
    16,
    17,
    17,
    18,
    18,
    19,
    19,
    20,
    20,
    21,
    21,
    22,
    22,
    23,
    24,
    24,
    25,
    25,
    26,
    27,
    27,
    28,
    29,
    29,
    30,
    31,
    32,
    32,
    33,
    34,
    35,
    35,
    36,
    37,
    38,
    39,
    39,
    40,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    50,
    51,
    52,
    54,
    55,
    56,
    57,
    58,
    59,
    60,
    61,
    62,
    63,
    64,
    66,
    67,
    68,
    69,
    70,
    72,
    73,
    74,
    75,
    77,
    78,
    79,
    81,
    82,
    83,
    85,
    86,
    87,
    89,
    90,
    92,
    93,
    95,
    96,
    98,
    99,
    101,
    102,
    104,
    105,
    107,
    109,
    110,
    112,
    114,
    115,
    117,
    119,
    120,
    122,
    124,
    126,
    127,
    129,
    131,
    133,
    135,
    137,
    138,
    140,
    142,
    144,
    146,
    148,
    150,
    152,
    154,
    156,
    158,
    160,
    162,
    164,
    167,
    169,
    171,
    173,
    175,
    177,
    180,
    182,
    184,
    186,
    189,
    191,
    193,
    196,
    198,
    200,
    203,
    205,
    208,
    210,
    213,
    215,
    218,
    220,
    223,
    225,
    228,
    231,
    233,
    236,
    239,
    241,
    244,
    247,
    249,
    252,
    255,
]
