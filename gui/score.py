import pickle
from os.path import isfile

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QWidget

from gui.record_table import RecordTable


class Score(QWidget):
    """Реализует игровой счёт."""

    def __init__(self):
        # TODO перенести отсюда логику в другой пакет
        super().__init__()
        self.setFixedSize(100, 50)
        self.score = 0
        self.records = []
        self.record_table = None

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp: QPainter):
        """Отрисовывает счёт."""
        qp.drawText(0, 35, 'Score: {}'.format(self.score))

    def add_new_record(self):
        """Записывает новый рекорд."""
        # TODO оптимизировать структуру данных (кортеж)
        # TODO проверить корректность
        filename = "self.records.pickle"
        if isfile(filename):
            with open(filename, 'rb') as file:
                self.records = pickle.load(file)
        else:
            self.records = []

        min_score = self.records[-1][1] if self.records else 0
        scores = [record[1] for record in self.records if self.records]
        if self.score > min_score and self.score not in scores or \
           len(self.records) < 10 and self.score not in scores:
            window = QInputDialog()
            username, _ = window.getText(self, 'Score', 'Enter your name: ')
            if username:
                self.records.append((username, self.score))
            self.records.sort(key=lambda x: x[1], reverse=True)
            with open(filename, 'wb') as f:
                pickle.dump(self.records[:10], f)
            self.watch_record_table()
        # if self.records:
        #     for record in self.records:
        #         if self.score > record[1]:
        #             self._add_new_record(filename)
        #         else:
        #             continue
        #     if len(self.records) < 10:
        #         for record in self.records:
        #             if record[1] == self.score:
        #                 continue
        #             else:
        #                 self._add_new_record(filename)
        # else:
        #     self._add_new_record(filename)
    #
    # def _add_new_record(self, filename: str):
    #     window = QInputDialog()
    #     username, _ = window.getText(self, 'Score', 'Enter your name: ')
    #     if username:
    #         self.records.append((username, self.score))
    #     self.records.sort(key=lambda x: x[1], reverse=True)
    #     with open(filename, 'wb') as f:
    #         pickle.dump(self.records[:10], f)
    #     self.watch_record_table()

    def watch_record_table(self):
        with open("self.records.pickle", 'rb') as f:
            records = pickle.load(f)
            # print(len(records))
            self.record_table = RecordTable(records)
            self.record_table.show()

    def redraw(self, score):
        """Перерисовывает игровой счёт."""
        self.score = score
        self.update()
