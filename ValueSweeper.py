import sys

class ValueSweeperBase:
    def reset(self):
        pass

    def is_at_end(self) -> bool:
        return True

    def advance(self) -> bool:
        return True

class ValueSweeper(ValueSweeperBase):
    base: int = 0,
    relative_min: int = 0,
    relative_max: int = 0,
    absolute_min: int = -sys.maxsize - 1
    absolute_max: int = sys.maxsize
    step: int = 1,
    enabled: bool = True,

    current_value: int = 0,

    def __init__(self,
                 base: int = 0,
                 relative_min: int = 0,
                 relative_max: int = 0,
                 step: int = 1,
                 enabled: bool = True):
        self.base = base
        self.relative_min = relative_min
        self.relative_max = relative_max
        self.step = step
        self.enabled = enabled

        self.reset()

    def get_lower_bound(self) -> int:
        return max(self.absolute_min, self.base - self.relative_min)

    def get_upper_bound(self) -> int:
        return min(self.absolute_max, self.base + self.relative_max)

    def get_range(self) -> int:
        return self.get_upper_bound() - self.get_lower_bound()

    # Based on the step size, what is the true end value
    def get_end_value(self) -> int:
        return self.get_upper_bound() - self.get_range() % self.step

    def is_at_end(self) -> bool:
        if self.enabled:
            return self.current_value >= self.get_end_value()
        else:
            return True

    def reset(self):
        if self.enabled:
            self.current_value = self.base - self.relative_min
        else:
            self.current_value = self.base

    # returns true if reset itself while advancing
    def advance(self) -> bool:
        if not self.enabled:
            return True

        if self.is_at_end():
            self.reset()
            return True
        else:
            self.current_value += self.step
            return False

class ValueSweeperCollection(ValueSweeperBase):
    value_sweepers: list[ValueSweeper]

    def reset(self):
        for value_sweeper in self.value_sweepers:
            value_sweeper.reset()

    def is_at_end(self) -> bool:
        for value_sweeper in self.value_sweepers:
            if not value_sweeper.is_at_end():
                return False

        return True

    def advance(self) -> bool:
        for value_sweeper_index in range(len(self.value_sweepers) -1, -1):
            if not self.value_sweepers[value_sweeper_index].advance():
                return False

        return True