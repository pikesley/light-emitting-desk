from unittest import TestCase
from unittest.mock import MagicMock, call, patch

with patch.dict(
    "utils.conf",
    {"segments": {"back-of-desk": [[0, 47]], "monitor": [[53, 60], [48, 52]]}},
    clear=True,
):
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

    def test_fill(self):
        """Test we can fill all the pixels."""
        desk = Desk({"foo": [[0, 19]]})
        desk.pixels = MagicMock()
        desk.fill([255, 0, 0])
        desk.pixels.assert_has_calls([call.fill([255, 0, 0]), call.show()])

    def test_light_up(self):
        """Test it calls a LightMode."""
        desk = Desk({"foo": [[0, 19]]})
        desk.light_up([0, 0, 255], {"mode": "converge"})
        # I'm not testing anything here wtf
