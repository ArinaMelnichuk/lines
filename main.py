from sys import exit, argv
import argparse

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from gui.gui import GUI
from gui.score import Score
from logic.field import Field


class SizeAction(argparse.Action):

    def __call__(self, parser, namespace, value, option_string=None):
        value = int(value)
        if value < 3:
            parser.error("invalid size")
        setattr(namespace, self.dest, value)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--field-size', help='sets the field size (NxN)',
                        dest='--field-size', metavar='FIELD-SIZE', type=int,
                        default=9, action=SizeAction)
    parser.add_argument('--cell-size', help='sets the cell size (it is \
        recommended to use the default parameter)', dest='--cell-size',
                        metavar='CELL-SIZE', type=int, default=60,
                        action=SizeAction)
    args = parser.parse_args()
    return args


class MainApplication(QWidget):
    """Вспомогательный класс для запуска программы."""

    def __init__(self, args):
        # TODO добавить тесты
        super().__init__()
        lo = QVBoxLayout()

        self.score = Score()
        self.field = Field(getattr(args, '--field-size'))
        self.gui = GUI(getattr(args, '--cell-size'), self.field, self.score)
        self.restart_button = QPushButton('Restart')
        self.watch_records_button = QPushButton('Record Table')
        self.watch_records_button.clicked.\
            connect(self.score.watch_record_table)
        self.restart_button.clicked.connect(self.gui.restart)

        lo.addWidget(self.score)
        lo.addWidget(self.gui)
        lo.addWidget(self.restart_button)
        lo.addWidget(self.watch_records_button)
        self.setLayout(lo)
        self.setWindowTitle('Lines')
        # подумать, как исправить
        self.setFixedSize(self.sizeHint())


if __name__ == '__main__':

    app = QApplication(argv)
    arguments = parse()
    window = MainApplication(arguments)
    window.show()
    exit(app.exec_())
