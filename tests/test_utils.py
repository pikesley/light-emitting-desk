from unittest.mock import patch

from utils import gamma_correct, random_colour, total_pixels

fake_conf = {"segments": {"back-of-desk": [[0, 47]], "monitor": [[76, 99], [48, 75]]}}


@patch.dict("utils.conf", fake_conf, clear=True)
def test_total_pixels():
    """Test it calculates the correct number of Pixels."""
    assert total_pixels() == 100


def test_gamma_correction():
    """Test it gamma-corrects correctly."""
    cases = (
        ([0, 0, 0], [0, 0, 0]),
        ([255, 255, 255], [255, 255, 255]),
        ([255, 0, 255], [255, 0, 255]),
        ([12, 34, 56], [0, 1, 4]),
        ([112, 134, 156], [25, 42, 64]),
        ([250, 251, 252], [241, 244, 247]),
    )

    for colour, corrected in cases:
        assert gamma_correct(colour) == corrected


def test_random_colour():
    """Test it generates sane random colours."""
    for _ in range(0, 100):
        colour = random_colour()
        for component in colour:
            assert 0 <= component <= 255

        weighted_colour = random_colour(127)
        for component in weighted_colour:
            assert 127 <= component <= 255
