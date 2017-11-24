from .ball_colors import BallColors
from .point import Point


class Ball:
    """Реализует игровой шарик."""

    def __init__(self, color: BallColors, position: Point):
        self.color = color
        self.position = position
