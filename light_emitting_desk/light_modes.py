import abc
from random import shuffle
from time import sleep

from light_emitting_desk.utils import conf, reorder_sequence_to_indeces


class LightMode:
    """Abstract class representing a lighting mode."""

    def __init__(self, desk, colour, args=None):
        """Construct."""
        self.desk = desk
        self.colour = colour

        self.args = conf["api"]["optional-fields"]
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


class Caterpillar(LightMode):
    """Caterpillar across the desk one pixel at a time."""

    def run(self):
        """Do the work."""
        starting_colour = self.desk[0]  # assume it's all one colour

        invert = False
        if "direction" in self.args:
            if self.args["direction"] == "backwards":
                invert = True

        for frame in caterpillar_iterator(
            starting_colour,
            self.colour,
            self.args["caterpillar-length"],
            self.desk.indeces,
            invert,
        ):
            for index, light in enumerate(frame):
                self.desk[index] = light

            self.show()
            self.wait()


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


def sequence_for_caterpillar(old, new, strip_length, cat_length):
    """Generate a sequence for a caterpillar across the desk."""
    frame = [old] * strip_length
    sequence = [frame.copy()]

    while not all([item == new for item in sequence[-1]]):
        next_set = caterpillar_sub_sequence(frame, new, cat_length)
        sequence.extend(next_set)
        frame = next_set[-1]

    return sequence


def caterpillar_sub_sequence(frame, new, cat_length):
    """Generate the steps for a given frame."""
    sub_sequence = []

    for index, _ in enumerate(frame):
        current = frame.copy()
        current[index] = new
        for cell in range(cat_length):
            tail_index = index - cell
            if tail_index >= 0:
                current[tail_index] = new

        sub_sequence.append(current)

        if all([item == new for item in current[index:]]):
            return sub_sequence


def caterpillar_iterator(old, new, cat_length, indeces, invert=False):
    """Iterate over the caterpillar-sequence."""
    for item in sequence_for_caterpillar(old, new, len(indeces), cat_length):
        if invert:
            item = list(reversed(item))
        yield reorder_sequence_to_indeces(item, indeces)
