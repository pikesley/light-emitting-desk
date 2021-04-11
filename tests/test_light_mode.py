from light_emitting_desk.light_modes import (caterpillar_iterator,
                                             caterpillar_sub_sequence,
                                             divergence_sequence_for_sectors,
                                             pairs_from_list,
                                             sequence_for_caterpillar)


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


def test_sequence_for_caterpillar():
    """Test it generates a caterpillar sequence."""
    cases = (
        (0, 1, 1, 1, [[0], [1]]),
        (0, 1, 2, 1, [[0, 0], [1, 0], [0, 1], [1, 1]]),
        (
            0,
            1,
            3,
            1,
            [
                [0, 0, 0],
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1],
                [1, 0, 1],
                [0, 1, 1],
                [1, 1, 1],
            ],
        ),
        (
            "a",
            "b",
            6,
            2,
            [
                ["a", "a", "a", "a", "a", "a"],
                ["b", "a", "a", "a", "a", "a"],
                ["b", "b", "a", "a", "a", "a"],
                ["a", "b", "b", "a", "a", "a"],
                ["a", "a", "b", "b", "a", "a"],
                ["a", "a", "a", "b", "b", "a"],
                ["a", "a", "a", "a", "b", "b"],
                ["b", "a", "a", "a", "b", "b"],
                ["b", "b", "a", "a", "b", "b"],
                ["a", "b", "b", "a", "b", "b"],
                ["a", "a", "b", "b", "b", "b"],
                ["b", "a", "b", "b", "b", "b"],
                ["b", "b", "b", "b", "b", "b"],
            ],
        ),
    )

    for old, new, strip_length, cat_length, expectation in cases:
        assert (
            sequence_for_caterpillar(old, new, strip_length, cat_length) == expectation
        )


def test_caterpillar_sub_sequence():
    """Test the per-frame sub-sequence."""
    cases = (
        ([0, 0], 1, 1, [[1, 0], [0, 1]]),
        ([0, 0, 0], 1, 1, [[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
        (
            [0, 0, 0, 0],
            1,
            1,
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
        ),
        ([0, 0, 0, 1], 1, 1, [[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]]),
        ([0, 0, 0, 1, 1], 1, 1, [[1, 0, 0, 1, 1], [0, 1, 0, 1, 1], [0, 0, 1, 1, 1]]),
        ([0, 0, 1, 1, 1], 1, 1, [[1, 0, 1, 1, 1], [0, 1, 1, 1, 1]]),
        ([0, 1, 1, 1, 1, 1], 1, 1, [[1, 1, 1, 1, 1, 1]]),
        (
            [0, 0, 0, 0],
            1,
            2,
            [[1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]],
        ),
        (
            [2, 2, 2, 2, 2, 2, 3, 3],
            3,
            3,
            [
                [3, 2, 2, 2, 2, 2, 3, 3],
                [3, 3, 2, 2, 2, 2, 3, 3],
                [3, 3, 3, 2, 2, 2, 3, 3],
                [2, 3, 3, 3, 2, 2, 3, 3],
                [2, 2, 3, 3, 3, 2, 3, 3],
                [2, 2, 2, 3, 3, 3, 3, 3],
            ],
        ),
    )

    for frame, new, cat_length, expectation in cases:
        assert caterpillar_sub_sequence(frame, new, cat_length) == expectation


def test_caterpillar_iterator():
    """Test it has an iterator."""
    results = []
    for frame in caterpillar_iterator(".", "O", 2, [0, 1, 5, 4, 2, 3]):
        results.append(frame)

    assert results == [
        [".", ".", ".", ".", ".", "."],
        ["O", ".", ".", ".", ".", "."],
        ["O", "O", ".", ".", ".", "."],
        [".", "O", ".", ".", "O", "."],
        [".", ".", ".", ".", "O", "O"],
        [".", ".", ".", "O", ".", "O"],
        [".", ".", "O", "O", ".", "."],
        ["O", ".", "O", "O", ".", "."],
        ["O", "O", "O", "O", ".", "."],
        [".", "O", "O", "O", "O", "."],
        [".", ".", "O", "O", "O", "O"],
        ["O", ".", "O", "O", "O", "O"],
        ["O", "O", "O", "O", "O", "O"],
    ]


def test_reversed_caterpillar_iterator():
    """Test the iterator reverses correctly."""
    results = []
    for frame in caterpillar_iterator(".", "O", 2, [0, 1, 5, 4, 2, 3], invert=True):
        results.append(frame)

    assert results == [
        [".", ".", ".", ".", ".", "."],
        [".", ".", "O", ".", ".", "."],
        [".", ".", "O", "O", ".", "."],
        [".", ".", ".", "O", ".", "O"],
        [".", ".", ".", ".", "O", "O"],
        [".", "O", ".", ".", "O", "."],
        ["O", "O", ".", ".", ".", "."],
        ["O", "O", "O", ".", ".", "."],
        ["O", "O", "O", "O", ".", "."],
        ["O", "O", ".", "O", ".", "O"],
        ["O", "O", ".", ".", "O", "O"],
        ["O", "O", "O", ".", "O", "O"],
        ["O", "O", "O", "O", "O", "O"],
    ]
