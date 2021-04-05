from unittest import TestCase
from unittest.mock import MagicMock, call

from light_emitting_desk.desk import Desk
from light_emitting_desk.light_modes import SectorDiverge


class TestSectorDiverge(TestCase):
    """Test `SectorDiverge`."""

    def test_sector_diverging(self):
        """Test it diverges per-sector."""
        desk = Desk({"back-of-desk": [[0, 4]], "monitor": [[9, 7], [6, 5]]})
        desk.pixels = MagicMock()
        diverge = SectorDiverge(desk, [0, 255, 0])
        diverge.run()

        desk.pixels.assert_has_calls(
            [
                call.__setitem__(2, [0, 255, 0]),
                call.__setitem__(5, [0, 255, 0]),
                call.__setitem__(6, [0, 255, 0]),
                call.__setitem__(8, [0, 255, 0]),
                call.show(),
                call.__setitem__(1, [0, 255, 0]),
                call.__setitem__(3, [0, 255, 0]),
                call.__setitem__(7, [0, 255, 0]),
                call.__setitem__(9, [0, 255, 0]),
                call.show(),
                call.__setitem__(0, [0, 255, 0]),
                call.__setitem__(4, [0, 255, 0]),
                call.show(),
            ]
        )
