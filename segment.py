from time import sleep

# from converger import Converger
from utils import gamma_correct


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

    # def settle_from_random(self, colour, steps, delay=0.1):
    #     """Set random pixels then converge on a single colour."""
    #     initial_state = []
    #     for _ in self.indeces:
    #         initial_state.append(random_colour())

    #     converger = Converger(initial_state, colour, steps)

    #     for frame in converger.frames():
    #         for j, colour in enumerate(frame):
    #             self.desk[j] = colour
    #         self.desk.show()
    #         sleep(delay)
