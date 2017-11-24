from enum import Enum
from PyQt5.QtGui import QColor


class BallColors(Enum):
    """Энум, содержащий все цвета шариков."""

    red = QColor(255, 0, 0)
    green = QColor(0, 255, 0)
    blue = QColor(0, 0, 255)
    yellow = QColor(255, 255, 0)
    pink = QColor(255, 0, 255)
    turquoise = QColor(0, 255, 255)
    purple = QColor(148, 0, 211)
