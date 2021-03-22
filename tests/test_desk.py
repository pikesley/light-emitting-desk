from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from desk import Desk


class TestDesk(TestCase):
    """Test the Desk."""

    @patch.dict(
        "utils.conf",
        {"segments": {"back-of-desk": [[0, 47]], "monitor": [[53, 60], [48, 52]]}},
        clear=True,
    )
    def test_constructor(self):
        """Test it gets the right data."""
        desk = Desk({"back-of-desk": [[0, 47]], "monitor": [[53, 60], [48, 52]]})
        self.assertCountEqual(desk.segments.keys(), ["back-of-desk", "monitor"])

        seg = desk.segments["monitor"]
        self.assertEqual(
            seg.indeces, [53, 54, 55, 56, 57, 58, 59, 60, 48, 49, 50, 51, 52]
        )

    def test_setting_lights(self):
        """Test we can set a light to a colour."""
        desk = Desk({"foo": [[0, 19]]})
        desk[19] = [255, 0, 0]
        desk.show()

        self.assertEqual(desk[19], [255, 0, 0])

    def test_sweep(self):
        """Test we can sweep across the whole desk."""
        desk = Desk({"back-of-desk": [[0, 4]], "monitor": [[9, 7], [6, 5]]})
        desk.pixels = MagicMock()
        desk.sweep([0, 255, 0])

        desk.pixels.assert_has_calls(
            [
                call.__setitem__(0, [0, 255, 0]),
                call.show(),
                call.__setitem__(1, [0, 255, 0]),
                call.show(),
                call.__setitem__(2, [0, 255, 0]),
                call.show(),
                call.__setitem__(3, [0, 255, 0]),
                call.show(),
                call.__setitem__(4, [0, 255, 0]),
                call.show(),
                call.__setitem__(9, [0, 255, 0]),
                call.show(),
                call.__setitem__(8, [0, 255, 0]),
                call.show(),
                call.__setitem__(7, [0, 255, 0]),
                call.show(),
                call.__setitem__(6, [0, 255, 0]),
                call.show(),
                call.__setitem__(5, [0, 255, 0]),
                call.show(),
            ]
        )

    def test_reverse_sweep(self):
        """Test we can sweep backwards across the whole desk."""
        desk = Desk({"back-of-desk": [[0, 4]], "monitor": [[9, 7], [6, 5]]})
        desk.pixels = MagicMock()
        desk.sweep([0, 255, 0], direction="backwards")

        desk.pixels.assert_has_calls(
            [
                call.__setitem__(5, [0, 255, 0]),
                call.show(),
                call.__setitem__(6, [0, 255, 0]),
                call.show(),
                call.__setitem__(7, [0, 255, 0]),
                call.show(),
                call.__setitem__(8, [0, 255, 0]),
                call.show(),
                call.__setitem__(9, [0, 255, 0]),
                call.show(),
                call.__setitem__(4, [0, 255, 0]),
                call.show(),
                call.__setitem__(3, [0, 255, 0]),
                call.show(),
                call.__setitem__(2, [0, 255, 0]),
                call.show(),
                call.__setitem__(1, [0, 255, 0]),
                call.show(),
                call.__setitem__(0, [0, 255, 0]),
                call.show(),
            ]
        )
