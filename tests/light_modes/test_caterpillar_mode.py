from unittest import TestCase

from light_emitting_desk.desk import Desk
from light_emitting_desk.light_modes import Caterpillar


class TestCaterpillar(TestCase):
    """Test `Caterpillar`."""

    def test_caterpillar(self):
        """Test it caterpillars."""
        desk = Desk({"back-of-desk": [[0, 4]], "monitor": [[9, 7], [6, 5]]})
        caterpillar = Caterpillar(desk, [255, 0, 0], {"delay": 0})
        caterpillar.run()

        self.assertTrue(all(pixel == [255, 0, 0] for pixel in desk.pixels))

    def test_reverse_caterpillar(self):
        """Test it caterpillars backwards."""
        desk = Desk({"back-of-desk": [[0, 4]], "monitor": [[9, 7], [6, 5]]})
        caterpillar = Caterpillar(
            desk, [255, 0, 0], {"delay": 0, "direction": "backwards"}
        )
        caterpillar.run()

        self.assertTrue(all(pixel == [255, 0, 0] for pixel in desk.pixels))
