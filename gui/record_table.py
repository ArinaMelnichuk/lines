from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout


class RecordTable(QWidget):
    """Реализует таблицу рекордов."""

    def __init__(self, records: list):
        super().__init__()
        lo = QVBoxLayout()

        self.setLayout(lo)
        self.setWindowTitle('Record Table')

        self.setFixedSize(250, 400)
        self.records = records

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp: QPainter):
        """Отрисовывает таблицу."""
        shift = 0
        for record in self.records:
            qp.drawText(40, 40 + shift, '{}: {}'.format(record[0], record[1]))
            shift += 35
