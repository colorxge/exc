class Progression:
    def __init__(self, start=0):
        self._current = start

    def _advence(self):
        self._current += 1

    def __next__(self):
        if self._current is None:
            raise StopIteration()
        else:
            answer = self._current
            self._advence()
            return answer

    def __iter__(self):
        return self

    def print_progression(self, n):
        print(' '.join(str(next(self)) for _ in range(n)))


class ArithmeticProgression(Progression):
    def __init__(self, increment=1, start=0):
        super().__init__(start)
        self._increment = increment

    def _advence(self):
        self._current += self._increment


class GeometricProgression(Progression):
    def __init__(self, base=2, start=1):
        super().__init__(start)
        self._base = base

    def _advence(self):
        self._current *= self._base


class FibonacciProgression(Progression):
    def __init__(self, first=0, second=1):
        super().__init__(first)
        self._prev = second -first

    def _advence(self):
        self._prev, self._current = self._current, self._prev +self._current

if __name__ == "__main__":
    a = FibonacciProgression(4, 7)
    print(a.print_progression(10))