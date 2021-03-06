from unittest.mock import patch

from light_emitting_desk.utils import (gamma_correct, random_colour,
                                       reorder_sequence_to_indeces,
                                       scale_colour, total_pixels)

fake_conf = {"sectors": {"back-of-desk": [[0, 47]], "monitor": [[76, 99], [48, 75]]}}
inverted_conf = {
    "sectors": {"back-of-desk": [[0, 47]], "monitor": [[99, 76], [75, 44]]}
}


@patch.dict("light_emitting_desk.utils.conf", fake_conf, clear=True)
def test_total_pixels():
    """Test it calculates the correct number of Pixels."""
    assert (
        total_pixels({"back-of-desk": [[0, 27]], "monitor": [[56, 67], [28, 55]]}) == 68
    )


@patch.dict("light_emitting_desk.utils.conf", inverted_conf, clear=True)
def test_total_pixels_when_inverted():
    """Test it gets the correct Pixel-count when the direction is reversed."""
    assert (
        total_pixels({"back-of-desk": [[0, 47]], "monitor": [[108, 76], [75, 44]]})
        == 109
    )


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


def test_scale_colour():
    """Test scaling a colour."""
    cases = (
        ([255, 255, 255], 1, [255, 255, 255]),
        ([255, 255, 255], 0, [0, 0, 0]),
        ([128, 200, 50], 0.5, [64, 100, 25]),
    )

    for colour, factor, expectation in cases:
        assert scale_colour(colour, factor) == expectation


def test_reorder_sequence_to_indeces():
    """Test it reorders a sequence for our indeces."""
    indeces = [0, 1, 2, 7, 6, 5, 3, 4, 8, 9]
    sequence = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

    assert reorder_sequence_to_indeces(sequence, indeces) == [
        "a",
        "b",
        "c",
        "h",
        "g",
        "f",
        "d",
        "e",
        "i",
        "j",
    ]
