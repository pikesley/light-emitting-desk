from rgb_desk.light_modes import (divergence_sequence_for_sectors,
                                  pairs_from_list)


def test_pairs_from_list():
    """Test it generates the pairs for from-each-end lighting."""
    cases = (
        ([0, 1], [[0, 1]]),
        ([0, 4, 1, 2, 5, 3], [[0, 3], [4, 5], [1, 2]]),
        ([7, 6, 3, 2, 0], [[7, 0], [6, 2], [3]]),
    )

    for lights, pairs in cases:
        assert pairs_from_list(lights) == pairs


def test_divergence_sequence_for_sectors():
    """Test it generates the indeces for divergence per-sector."""
    cases = (
        ([[0, 1, 2, 3]], [[1, 2], [0, 3]]),
        (
            [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]],
            [[1, 2, 5, 6, 9, 10], [0, 3, 4, 7, 8, 11]],
        ),
        (
            [[3, 2, 0, 1], [4, 7, 5, 6], [11, 10, 8, 9]],
            [[0, 2, 5, 7, 8, 10], [1, 3, 4, 6, 9, 11]],
        ),
        (
            [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]],
            [[2, 7], [1, 3, 6, 8], [0, 4, 5, 9]],
        ),
        ([[0, 1, 2], [4, 5, 6, 7, 8, 9]], [[1, 6, 7], [0, 2, 5, 8], [4, 9]]),
    )

    for sectors, sequence in cases:
        assert divergence_sequence_for_sectors(sectors) == sequence
