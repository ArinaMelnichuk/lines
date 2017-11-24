

class Point:
    """Реализует класс 'точка'."""

    def __init__(self, x: int, y: int):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError
        self.x = x
        self.y = y

    def __str__(self):
        return str.format('({}, {})', self.x, self.y)

    def __repr__(self):
        return str(self)
