from argparse import ArgumentParser

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QGridLayout,
    QDesktopWidget, QMessageBox
)

from src.cli import Parser
from .config_storage import ConfigStorage
from .grids import MainForm


class Gui(QWidget):

    window_h = 600
    window_w = 900
    in_work = False
    gui_params = None
    config_storage = None
    lang_btn = None
    quit_question = False
    provider = None

    def __init__(self, args: ArgumentParser):
        super().__init__()
        self.gui_params = {}
        self.args = args.parse_args()
        self.parser = Parser(args)
        self.config_storage = ConfigStorage()
        self.grids = MainForm(self)

    def print(self, text, end='\n'):
        self.gui_params['log'].insertHtml('{}{}'.format(text, end))

    def clear_log(self):
        self.gui_params['log'].setText('')

    def progress(self, items_count: int, current_item: int):
        pass

    def quest(self, variants: enumerate, title: str, select_type=0):  # 0 = single, 1 = multiple
        if select_type:
            return self._multiple_quest(variants, title)
        return self._single_quest(variants, title)

    def _translate(self, key):
        return self.config_storage.translate(key)

    def main(self):
        self.init_ui()
        self.show()
        self.center()

    def init_ui(self):
        global_grid = QGridLayout()
        _grid = QGridLayout()

        _grid.addLayout(self.grids.get_config_grid(), 0, 0)
        _grid.addLayout(self.grids.get_base_grid(),   0, 1)

        global_grid.addLayout(self.grids.get_uri_grid(), 0, 0)
        global_grid.addLayout(_grid, 1, 0)

        self.setLayout(global_grid)

        # self.setGeometry(300, 300, self.maxW, self.maxH)
        self.setMinimumWidth(self.window_w)
        self.setMinimumHeight(self.window_h)
        self.setMaximumWidth(self.window_w)
        self.setMaximumHeight(self.window_h)
        self.setWindowIcon(QIcon('docs/favicon.ico'))
        self.setWindowTitle('Manga downloader')

    def next_lang(self):
        lang = self.config_storage.next_lang()
        self.lang_btn.setText(lang)
        if not getattr(self, 'quit_question', False):
            self.quit_question = True
            quest = QMessageBox.information(
                self, 'Need restart',
                'For change language need restart',
                QMessageBox.Ok | QMessageBox.Ignore,
                QMessageBox.Ok
            )
            quest == QMessageBox.Ok and exit()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        pos = qr.topLeft()
        pos.setY(pos.y() + 20)
        self.move(pos)

    def closeEvent(self, event):
        if not self.in_work:
            event.accept()
            return

        reply = QMessageBox.question(
            self, 'Quit',
            "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def _multiple_quest(self, variants, title):
        pass

    def _single_quest(self, variants, title):
        pass

    def _run_downloader(self):

        # self.provider = self.parser.init_provider(
        #     progress_callback=self.progress,
        #     logger_callback=self.print,
        #     quest_callback=self.quest
        # )

        pass
