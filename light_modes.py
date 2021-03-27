import abc
from random import shuffle
from time import sleep

from utils import conf


class LightMode:
    """Abstract class representing a lighting mode."""

    def __init__(self, desk, colour, args=None):
        """Construct."""
        self.desk = desk
        self.colour = colour

        self.args = conf["light-mode-defaults"]
        if args:
            self.args = {**self.args, **args}

    def __setitem__(self, index, colour):
        """Override `x[i] = 'foo'`."""
        self.desk[index] = colour

    def show(self):
        """`show` the pixels."""
        self.desk.show()

    def wait(self):
        """Wait a bit."""
        sleep(self.args["delay"])

    @abc.abstractmethod
    def run(self):
        """Do the work."""
        return  # nocov


class Sweep(LightMode):
    """Sweep right across the Desk."""

    def run(self):
        """Do the work."""
        indeces = self.desk.indeces.copy()
        if "direction" in self.args:
            if self.args["direction"] == "backwards":
                indeces = reversed(indeces)

        for index in indeces:
            self[index] = self.colour
            self.show()
            self.wait()


class SpotFill(LightMode):
    """Fill random pixels until the desk is all the new colour."""

    def run(self):
        """Do the work."""
        indeces = self.desk.indeces.copy()
        shuffle(indeces)

        for index in indeces:
            self[index] = self.colour
            self.show()
            self.wait()


class Converge(LightMode):
    """Close in from both ends."""

    def run(self):
        """Do the work."""
        for pair in pairs_from_list(self.desk.indeces):
            for index in pair:
                self[index] = self.colour
            self.show()
            self.wait()


class SectorDiverge(LightMode):
    """Colour each sector by diverging from its centre."""

    def run(self):
        """Do the work."""
        for step in divergence_sequence_for_sectors(self.desk.sectors):
            for index in step:
                self[index] = self.colour

            self.show()
            self.wait()


class DirectSwitch(LightMode):
    """Just colour all the pixels at once."""

    def run(self):
        """Do the work."""
        self.desk.fill(self.colour)


###


def pairs_from_list(lights):
    """Generate a list of pairs to enable from-each-end lighting."""
    length = len(lights)
    half = int(length / 2)
    offset = 0

    centre = None
    if length % 2 == 1:
        centre = lights[half]
        offset = 1

    left = lights[:half]

    rh_start = half + offset
    right = reversed(lights[rh_start:])

    pairs = list(map(list, zip(left, right)))

    if centre:
        pairs.append([centre])

    return pairs


def divergence_sequence_for_sectors(sectors):
    """Generate a sequence for divergent lighting per-sector."""
    sequence = []
    pairs = map(pairs_from_list, sectors)
    for items in pairs:
        for j, pair in enumerate(reversed(items)):
            try:
                sequence[j].extend(pair)
            except IndexError:
                sequence.append(pair)

    # sort the member lists
    return list(map(sorted, sequence))
