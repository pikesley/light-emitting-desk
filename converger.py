class Converger:
    """Pull an arbitrary string of colours to a target colour."""

    def __init__(self, initial_state, target_colour, steps):
        """Construct."""
        self.initial_state = initial_state
        self.target_colour = target_colour
        self.steps = steps
        self.length = len(initial_state)

        self.increments = find_increments(
            self.initial_state, self.target_colour, self.steps
        )

    def frames(self):
        """Iterate over our frames."""
        current_state = self.initial_state

        for _ in range(0, self.steps):
            yield current_state

            next_state = []
            for j, colour in enumerate(current_state):
                new_colour = []
                for k, component in enumerate(colour):
                    new_component = int(component + self.increments[j][k])
                    if new_component > 255:
                        new_component = 255
                    if new_component < 0:
                        new_component = 0

                    new_colour.append(new_component)

                next_state.append(new_colour)

            current_state = next_state

        # at the end, return the final expectation
        yield [self.target_colour] * self.length


def get_increment(component, target, steps):
    """Calculate the increments needed to get `component` to `target` in `steps`."""
    if component > target:
        return 0 - (component - target) / steps

    return (target - component) / steps


def find_increments(initial_state, target_colour, steps):
    """Find the increments to get us to the target colour."""
    increments = []
    for colour in initial_state:
        increment_set = []
        for index, component in enumerate(colour):
            increment_set.append(get_increment(component, target_colour[index], steps))

        increments.append(increment_set)

    return increments
