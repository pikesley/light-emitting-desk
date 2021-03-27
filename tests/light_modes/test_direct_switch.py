from unittest import TestCase

from desk import Desk
from light_modes import DirectSwitch


class TestDirectSwitch(TestCase):
    """Test `DirectSwitch`."""

    def test_direct_switching(self):
        """Test it direct-switches."""
        desk = Desk({"back-of-desk": [[0, 4]], "monitor": [[9, 7], [6, 5]]})
        spot_fill = DirectSwitch(desk, [255, 0, 0], {"delay": 0})
        spot_fill.run()

        self.assertTrue(all(pixel == [255, 0, 0] for pixel in desk.pixels))
