from unittest import TestCase
from unittest.mock import MagicMock, call

from segment import Segment


class TestSegment(TestCase):
    """Test the Segment."""

    def test_constructor(self):
        """Test it gets the right data."""
        desk = MagicMock()
        seg = Segment("foo", [[10, 19], [0, 9]], desk)

        self.assertEqual(seg.name, "foo")
        self.assertEqual(
            seg.indeces,
            [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        )

    def test_sweeping(self):
        """Test it lights the right pixels."""
        desk = MagicMock()
        seg = Segment("bar", [[2, 3], [0, 1]], desk)

        seg.sweep([255, 0, 0])
        desk.assert_has_calls(
            [
                call.__setitem__(2, [255, 0, 0]),
                call.show(),
                call.__setitem__(3, [255, 0, 0]),
                call.show(),
                call.__setitem__(0, [255, 0, 0]),
                call.show(),
                call.__setitem__(1, [255, 0, 0]),
                call.show(),
            ]
        )

    def test_reverse_sweeping(self):
        """Test it lights the right pixels."""
        desk = MagicMock()
        seg = Segment("baz", [[12, 13], [10, 11]], desk)

        seg.sweep([255, 0, 0], direction="backwards")
        desk.assert_has_calls(
            [
                call.__setitem__(11, [255, 0, 0]),
                call.show(),
                call.__setitem__(10, [255, 0, 0]),
                call.show(),
                call.__setitem__(13, [255, 0, 0]),
                call.show(),
                call.__setitem__(12, [255, 0, 0]),
                call.show(),
            ]
        )
