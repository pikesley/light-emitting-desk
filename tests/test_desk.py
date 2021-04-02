from unittest import TestCase
from unittest.mock import MagicMock, call, patch

with patch.dict(
    "rgb_desk.utils.conf",
    {"sectors": {"back-of-desk": [[0, 47]], "monitor": [[53, 60], [48, 52]]}},
    clear=True,
):
    from rgb_desk.desk import Desk


class TestDesk(TestCase):
    """Test the Desk."""

    @patch.dict(
        "rgb_desk.utils.conf",
        {"sectors": {"back-of-desk": [[0, 47]], "monitor": [[53, 60], [48, 52]]}},
        clear=True,
    )
    def test_constructor(self):
        """Test it gets the right data."""
        desk = Desk({"back-of-desk": [[0, 7]], "monitor": [[13, 11], [8, 10]]})

        self.assertEqual(
            desk.sectors, [[0, 1, 2, 3, 4, 5, 6, 7], [13, 12, 11], [8, 9, 10]]
        )
        self.assertEqual(desk.indeces, [0, 1, 2, 3, 4, 5, 6, 7, 13, 12, 11, 8, 9, 10])

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
