from unittest import TestCase

from rgb_desk.desk import Desk
from rgb_desk.light_modes import SpotFill


class TestSpotFill(TestCase):
    """Test `SpotFill`."""

    def test_spot_filling(self):
        """Test it spot-fills."""
        desk = Desk({"back-of-desk": [[0, 4]], "monitor": [[9, 7], [6, 5]]})
        spot_fill = SpotFill(desk, [255, 0, 0], {"delay": 0})
        spot_fill.run()

        self.assertTrue(all(pixel == [255, 0, 0] for pixel in desk.pixels))
