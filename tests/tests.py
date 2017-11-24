import unittest

from math import ceil

from gui.gui import GUI
from gui.score import Score
from logic.ball import Ball
from logic.ball_colors import BallColors
from logic.field import Field
from logic.point import Point


class LinesTestCase(unittest.TestCase):

    def test_raises_exception(self):
        with self.assertRaises(ValueError):
            board = Field(2)
            board = Field(-1)
            gui = GUI(1, Field(9), Score())
            gui = GUI(-1, Field(9), Score())

    def test_find_lines(self):
        sizes = [size for size in range(4, 20)]
        for field_size in sizes:
            field = Field(field_size)
            field.field_objects = [[None] * field_size for _
                                   in range(field_size)]
            for component in range(field.min_line_size):
                field.field_objects[component][0] = Ball(BallColors.blue,
                                                         Point(component, 0))
                field.field_objects[field_size - 1][component] = Ball(
                    BallColors.green, Point(field_size - 1, component))
                field.field_objects[component][field_size - component - 1] = \
                    Ball(BallColors.red, Point(component,
                                               field_size - component - 1))
            field.remove_lines_and_rectangles()
            balls = [(field.field_objects[component][0], field.field_objects
                     [field_size - 1][component],
                      field.field_objects[component]
                      [field_size - component - 1])
                     for component in range(field.min_line_size)]
            self.assertFalse(any(any(ball) for ball in balls))

    def test_find_rectangles(self):
        sizes = [size for size in range(4, 20)]
        for field_size in sizes:
            field = Field(field_size)
            field.field_objects = [[None] * field_size for _
                                   in range(field_size)]
            for x in range(ceil((field.min_line_size + 1) / 2)):
                for y in range(ceil((field.min_line_size + 1) / 2)):
                    field.field_objects[x][y] = Ball(BallColors.blue,
                                                     Point(x, y))
            field.remove_lines_and_rectangles()
            balls = (field.field_objects[x][y] for x in range(
                ceil((field.min_line_size + 1) / 2)
                    ) for y in range(ceil((field.min_line_size + 1) / 2)))
            self.assertFalse(any(balls))

if __name__ == '__main__':
    unittest.main()
