from unittest import TestCase
from unittest.mock import patch

from desk import Desk

fake_conf = {"segments": {"back-of-desk": [[0, 47]], "monitor": [[53, 60], [48, 52]]}}


@patch.dict("utils.conf", fake_conf, clear=True)
class TestDesk(TestCase):
    """Test the Desk."""

    def test_constructor(self):
        """Test it gets the right data."""
        desk = Desk()
        self.assertCountEqual(desk.segments.keys(), ["back-of-desk", "monitor"])

        seg = desk.segments["monitor"]
        self.assertEqual(
            seg.indeces, [53, 54, 55, 56, 57, 58, 59, 60, 48, 49, 50, 51, 52]
        )

    def test_setting_lights(self):
        """Test we can set a light to a colour."""
        desk = Desk()
        desk[19] = [255, 0, 0]
        desk.show()

        self.assertEqual(desk[19], [255, 0, 0])
