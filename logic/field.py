from math import ceil, floor
from random import choice

from .ball import Ball
from .ball_colors import BallColors
from .point import Point


class Field:
    """Реализует логику игры."""

    def __init__(self, field_size: int):
        # некорректно рассчитывается счёт
        # Минимальная линия -- вверх n/2 + eps
        # выгоднее уничтожить 5 линий по 6, чем 6 линий по 5
        # выгоднее уничтожать подряд
        self.buffer = []
        self.len_buffer = []    # длины всех найденных линий и прямоугольников
        self.size = field_size
        self.min_line_size = ceil(field_size / 2 + 1e-6)
        self.field_objects = [[None] * field_size for _ in range(field_size)]
        self.game_over = False
        self.score = 0
        self.generate_balls(self.min_line_size + 1)

    def restart(self):
        """Вызывается в случае перезапуска игры, обнуляет все показатели."""
        self.buffer = []
        self.len_buffer = []
        self.field_objects = [[None] * self.size for _ in range(self.size)]
        self.game_over = False
        self.score = 0
        self.generate_balls(self.min_line_size + 1)

    def mouse_click(self, x, y):
        """Обрабатывает нажатие клавиши."""
        if not self.buffer:
            if self.field_objects[x][y]:
                self.buffer.append((x, y))
        else:
            if (x, y) == self.buffer[0]:
                self.buffer = []
            elif not self.field_objects[x][y]:
                self.buffer.append((x, y))
                self.swap()
            else:
                self.buffer[0] = (x, y)

    def get_balls(self):
        """Возвращает шарики, находящиеся на поле."""
        return (self.field_objects[x][y] for x in range(self.size) for y in
                range(self.size) if self.field_objects[x][y])

    def get_empty_cells(self):
        """Возвращает пустые клетки поля."""
        return ((x, y) for x in range(self.size) for y in range(self.size)
                if not self.field_objects[x][y])

    def swap(self):
        """Реализует перемещение шариков по полю."""
        (x1, y1), (x2, y2) = self.buffer
        if (x2, y2) in self.get_component(x1, y1):
            self.field_objects[x2][y2] = self.field_objects[x1][y1]
            self.field_objects[x1][y1] = None
            self.field_objects[x2][y2].position = Point(x2, y2)
            self.buffer = []

            if not self.remove_lines_and_rectangles():
                self.generate_balls(ceil(self.min_line_size / 2 + 1e-6))
                self.remove_lines_and_rectangles()
            if not list(self.get_empty_cells()):
                self.game_over = True
        else:
            self.buffer.pop()

    def get_component(self, x, y):
        """Возвращает вершины компоненты связности."""
        res = []
        stack = [(x, y)]
        while stack:
            x, y = stack.pop()
            res.append((x, y))
            yield x, y
            for _x in range(-1, 2):
                for _y in range(-1, 2):
                    if (abs(_x), abs(_y)) == (1, 1):
                        continue
                    n_x, n_y = x + _x, y + _y
                    if 0 <= n_x < self.size and 0 <= n_y < self.size and \
                            not self.field_objects[n_x][n_y] and (n_x, n_y) \
                            not in res:
                        stack.append((n_x, n_y))

    def find_lines_and_rectangles(self):
        """Ищет линии и прямоугольники."""
        ball_positions = set(map(lambda p: (p.position.x, p.position.y),
                                 self.get_balls()))
        result = set()
        colors_corresponding_balls = {}
        for color in BallColors:
            colors_corresponding_balls[color] = {(x, y)
                                                 for x, y in ball_positions
                                                 if self.field_objects[x][y].
                                                 color is color}
        for color_positions in colors_corresponding_balls.values():
            for x1, y1 in color_positions:
                for x2, y2 in color_positions - {(x1, y1)}:
                    r_x, r_y = abs(x1 - x2) + 1, abs(y1 - y2) + 1
                    min_x, min_y = min(x1, x2), min(y1, y2)
                    rect = {(min_x + x, min_y + y)
                            for x in range(r_x) for y in range(r_y)}
                    if rect.issubset(color_positions) and \
                       len(rect) >= self.min_line_size:
                        result.update(rect)
                    if r_x == r_y:
                        r_x = range(x1, x2 + 1) if x1 < x2 else \
                            range(x1, x2 - 1, -1)
                        r_y = range(y1, y2 + 1) if y1 < y2 else \
                            range(y1, y2 - 1, -1)
                        diagonal = {(x, y) for x, y in zip(r_x, r_y)}
                        if diagonal.issubset(color_positions) and \
                           len(diagonal) >= self.min_line_size:
                            result.update(diagonal)
        return result

    def generate_balls(self, n):
        """Генерирует шарики на поле."""
        # проверить, чтобы выгоднее было уничтожать подряд
        if self.len_buffer and len(self.len_buffer) != 1:
            first = sum(self.len_buffer) / len(self.len_buffer)
            second = len(self.len_buffer)
            self.score += floor(first) + second
            if first - 1 == second:
                self.score += self.min_line_size // 2
        empty_cells = list(self.get_empty_cells())
        cells = set()
        if not empty_cells:
            self.game_over = True
        while len(cells) < min(n, len(empty_cells)):
            cells.add(choice(empty_cells))
        for x, y in cells:
            colors = [c for c in BallColors]
            color = choice(colors)
            self.field_objects[x][y] = Ball(color, Point(x, y))
        self.len_buffer = []

    def remove_lines_and_rectangles(self):
        """Удаляет линии и прямоугольники с поля."""
        lines_and_rectangles = self.find_lines_and_rectangles()
        for x, y in lines_and_rectangles:
            self.field_objects[x][y] = None
        if lines_and_rectangles:
            self.len_buffer.append(len(lines_and_rectangles))
            self.score += len(lines_and_rectangles) * 2
        return lines_and_rectangles
