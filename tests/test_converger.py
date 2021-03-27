# from unittest import TestCase

# from converger import Converger, get_increment


# class TestConverger(TestCase):
#     """Test the Converger."""

#     def test_constructor(self):
#         """Test it gets the right data."""
#         initial = [[159, 220, 237], [159, 220, 237], [159, 220, 237], [159, 220, 237]]
#         conv = Converger(
#             initial,
#             [127, 0, 0],
#             10,
#         )
#         self.assertEqual(conv.initial_state, initial)
#         self.assertEqual(conv.target_colour, [127, 0, 0])
#         self.assertEqual(conv.steps, 10)

#     def test_increment_finding(self):
#         """Test it works out the correct increments."""
#         initial = [[200, 200, 200], [100, 100, 100], [150, 150, 150]]
#         conv = Converger(initial, [150, 150, 150], 4)
#         self.assertEqual(
#             conv.increments, [[-12.5, -12.5, -12.5], [12.5, 12.5, 12.5], [0, 0, 0]]
#         )

#     def test_realistic_increment_finding(self):
#         """Test it works out the correct increments for arbitrary values."""
#         initial = [[243, 17, 28], [30, 193, 234], [191, 136, 210], [47, 38, 74]]
#         conv = Converger(
#             initial,
#             [159, 220, 237],
#             13,
#         )
#         self.assertEqual(
#             conv.increments,
#             [
#                 [-6.461538461538462, 15.615384615384615, 16.076923076923077],
#                 [9.923076923076923, 2.076923076923077, 0.23076923076923078],
#                 [-2.4615384615384617, 6.461538461538462, 2.076923076923077],
#                 [8.615384615384615, 14.0, 12.538461538461538],
#             ],
#         )

#     def test_one_step_one_item(self):
#         """Test it moves one step for a one-item string."""
#         conv = Converger([[255, 255, 255]], [0, 0, 0], 1)

#         frames = []

#         for frame in conv.frames():
#             frames.append(frame)

#         self.assertEqual(frames, [[[255, 255, 255]], [[0, 0, 0]]])

#     def test_one_step_two_items(self):
#         """Test it moves one step for a two-item string."""
#         conv = Converger([[255, 255, 255], [127, 127, 127]], [0, 0, 0], 1)

#         frames = []

#         for frame in conv.frames():
#             frames.append(frame)

#         self.assertEqual(
#             frames, [[[255, 255, 255], [127, 127, 127]], [[0, 0, 0], [0, 0, 0]]]
#         )

#     def test_two_steps_one_item(self):
#         """Test it moves two steps for a one-item string."""
#         conv = Converger([[255, 255, 255]], [0, 0, 0], 2)

#         frames = []

#         for frame in conv.frames():
#             frames.append(frame)

#         self.assertEqual(frames, [[[255, 255, 255]], [[127, 127, 127]], [[0, 0, 0]]])

#     def test_four_steps_one_item(self):
#         """Test it moves four steps for a one-item string."""
#         conv = Converger([[4, 4, 4]], [0, 0, 0], 4)

#         frames = []

#         for frame in conv.frames():
#             frames.append(frame)

#         self.assertEqual(
#             frames, [[[4, 4, 4]], [[3, 3, 3]], [[2, 2, 2]], [[1, 1, 1]], [[0, 0, 0]]]
#         )

#     def test_one_step_one_item_from_below(self):
#         """Test it moves _up_ one step for a one-item string."""
#         conv = Converger([[0, 0, 0]], [255, 255, 255], 1)

#         frames = []

#         for frame in conv.frames():
#             frames.append(frame)

#         self.assertEqual(frames, [[[0, 0, 0]], [[255, 255, 255]]])

#     def test_two_steps_one_item_from_below(self):
#         """Test it moves _up_ one step for a one-item string."""
#         conv = Converger([[0, 0, 0]], [255, 255, 255], 2)

#         frames = []

#         for frame in conv.frames():
#             frames.append(frame)

#         self.assertEqual(frames, [[[0, 0, 0]], [[127, 127, 127]], [[255, 255, 255]]])

#     def test_four_steps_one_item_from_below(self):
#         """Test it moves up four steps for a one-item string."""
#         conv = Converger([[0, 0, 0]], [4, 4, 4], 4)

#         frames = []

#         for frame in conv.frames():
#             frames.append(frame)

#         self.assertEqual(
#             frames,
#             [
#                 [[0, 0, 0]],
#                 [[1, 1, 1]],
#                 [[2, 2, 2]],
#                 [[3, 3, 3]],
#                 [[4, 4, 4]],
#             ],
#         )

#     def test_with_nowhere_to_go(self):
#         """Test it remains inert when there's no change required."""
#         conv = Converger([[127, 127, 127]], [127, 127, 127], 4)

#         frames = []

#         for frame in conv.frames():
#             frames.append(frame)

#         self.assertEqual(
#             frames,
#             [
#                 [[127, 127, 127]],
#                 [[127, 127, 127]],
#                 [[127, 127, 127]],
#                 [[127, 127, 127]],
#                 [[127, 127, 127]],
#             ],
#         )

#     def test_with_four_bigger_steps(self):
#         """Test it moves down sensibly with arbitrary-sized steps."""
#         conv = Converger([[234, 15, 127]], [35, 183, 127], 4)

#         frames = []

#         for frame in conv.frames():
#             frames.append(frame)

#         self.assertEqual(
#             frames,
#             [
#                 [[234, 15, 127]],
#                 [[184, 57, 127]],
#                 [[134, 99, 127]],
#                 [[84, 141, 127]],
#                 [[35, 183, 127]],
#             ],
#         )

#     def test_a_mix_of_modes(self):
#         """Test it moves as expected for a more realistic string."""
#         initial_state = [[243, 17, 28], [30, 193, 234], [191, 136, 210], [47, 38, 74]]
#         target_colour = [18, 146, 244]
#         steps = 8

#         conv = Converger(initial_state, target_colour, steps)

#         frames = []

#         for frame in conv.frames():
#             frames.append(frame)

#         self.assertEqual(
#             frames,
#             [
#                 [[243, 17, 28], [30, 193, 234], [191, 136, 210], [47, 38, 74]],
#                 [[214, 33, 55], [28, 187, 235], [169, 137, 214], [43, 51, 95]],
#                 [[185, 49, 82], [26, 181, 236], [147, 138, 218], [39, 64, 116]],
#                 [[156, 65, 109], [24, 175, 237], [125, 139, 222], [35, 77, 137]],
#                 [[127, 81, 136], [22, 169, 238], [103, 140, 226], [31, 90, 158]],
#                 [[98, 97, 163], [20, 163, 239], [81, 141, 230], [27, 103, 179]],
#                 [[69, 113, 190], [18, 157, 240], [59, 142, 234], [23, 116, 200]],
#                 [[40, 129, 217], [16, 151, 241], [37, 143, 238], [19, 129, 221]],
#                 [[18, 146, 244], [18, 146, 244], [18, 146, 244], [18, 146, 244]],
#             ],
#         )


# def test_get_increment():
#     """Test the increment-finder."""
#     cases = (
#         (10, 0, 1, -10),
#         (10, 0, 2, -5),
#         (100, 25, 3, -25),
#         (101, 19, 7, -11),
#         (19, 101, 7, 11),
#         (3, 241, 13, 18),
#         (25, 25, 23, 0),
#     )

#     for component, target, steps, expectation in cases:
#         assert int(get_increment(component, target, steps)) == expectation
