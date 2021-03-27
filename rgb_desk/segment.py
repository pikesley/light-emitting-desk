from time import sleep

from rgb_desk.utils import gamma_correct


class Segment:
    """A segment of NeoPixels."""

    def __init__(self, name, sectors, desk):
        """Construct."""
        self.name = name

        self.indeces = []
        for sector in sectors:
            step = offset = 1
            if sector[0] > sector[1]:
                step = offset = -1

            self.indeces.extend(list(range(sector[0], sector[1] + offset, step)))

        self.desk = desk

    def sweep(self, colour, delay=0.01, direction="forwards"):
        """Sweep a colour across the segment."""
        indeces = self.indeces
        if direction == "backwards":
            indeces = reversed(indeces)

        colour = gamma_correct(colour)

        for i in indeces:
            self.desk[i] = colour
            self.desk.show()
            sleep(delay)