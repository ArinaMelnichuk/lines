from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget

from gui.score import Score
from logic.field import Field


class GUI(QWidget):
    """Реализует игровую графику."""

    def __init__(self, cell_size: int, field: Field, score: Score):
        if not isinstance(field, Field) or not isinstance(score, Score):
            raise TypeError
        super().__init__()
        self.cells_count = field.size
        self.cell_size = cell_size
        self.field = field
        self.score = score
        self.setFixedSize(self.cell_size * self.cells_count + 1,
                          self.cell_size * self.cells_count + 1)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_grid(qp)
        qp.end()

    def mousePressEvent(self, e):
        x = e.x() // self.cell_size
        y = e.y() // self.cell_size
        self.field.mouse_click(x, y)
        self.update()
        self.score.redraw(self.field.score)
        if self.field.game_over:
            print("Game over!")
            self.score.add_new_record()

    def draw_grid(self, qp):
        """Рисует игровое поле."""
        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(0, 0, self.cell_size * self.cells_count,
                    self.cell_size * self.cells_count)
        qp.setPen(QColor(0, 0, 0))
        for x in range(self.cells_count + 1):
            height = length = x * self.cell_size
            qp.drawLine(height, 0, height, self.cells_count * self.cell_size)
            qp.drawLine(0, length, self.cells_count * self.cell_size, length)
        if self.field.buffer:
            x, y = self.field.buffer[0]
            qp.setBrush(QColor(255, 235, 105))
            qp.drawRect(x * self.cell_size, y * self.cell_size, self.cell_size,
                        self.cell_size)
        for ball in self.field.get_balls():
            qp.setBrush(ball.color.value)
            qp.drawEllipse(
                ball.position.x * self.cell_size + self.cell_size // 4,
                ball.position.y * self.cell_size + self.cell_size // 4,
                self.cell_size // 2,
                self.cell_size // 2
            )

    def restart(self):
        """Перезапускает игру."""
        self.field.restart()
        self.score.redraw(self.field.score)
        self.update()
