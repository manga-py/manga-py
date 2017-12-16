from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QCheckBox,
     QDesktopWidget, QMessageBox, QSpinBox, QTextEdit, QGridLayout,
     QPushButton)
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.Qt import Qt
from argparse import ArgumentParser
from libs.gui import config_storage
from libs.cli import Parser


class Gui(QWidget):

    window_h = 600
    window_w = 900
    in_work = False
    gui_params = {}
    config_storage = None
    lang_btn = None

    def __init__(self, args: ArgumentParser):
        super().__init__()
        self.args = args.parse_args()
        self.parser = Parser(args)
        self.parser.set_logger_callback(self.print)
        self.parser.set_progress_callback(self.progress)
        self.config_storage = config_storage.ConfigStorage()

    def print(self, text):
        pass

    def progress(self, items_count: int, current_item: int):  # pragma: no cover
        pass

    def _translate(self, key):
        return self.config_storage.translate(key)

    def main(self):
        self.init_ui()
        self.show()
        self.center()

    def get_base_grid(self):

        self.gui_params['log'] = QTextEdit()
        self.gui_params['log'].setReadOnly(True)

        grid = QGridLayout()
        grid.setSpacing(10)

        btn = QPushButton('Run', self)
        btn.clicked.connect(self._run_downloader)
        btn.resize(btn.sizeHint())

        grid.addWidget(self.gui_params['log'], 0, 0, 5, 3)

        # self.gui_params['log'].insertHtml('<span style="color:red">asdasd</span><br>')

        grid.addWidget(btn, 6, 1, 1, 1)

        return grid

    def get_config_grid(self):
        destination_label = QLabel(self._translate('destination'))
        name_label = QLabel(self._translate('name'))
        skip_volumes_label = QLabel(self._translate('skip_volume'))
        max_volumes_label = QLabel(self._translate('max_volume'))
        reverse_label = QLabel(self._translate('reverse'))
        one_thread_label = QLabel(self._translate('one_thread'))

        self.gui_params['destination'] = QLineEdit()
        self.gui_params['name'] = QLineEdit()
        self.gui_params['skip_volumes'] = QSpinBox()
        self.gui_params['skip_volumes'].setRange(0, 999)
        self.gui_params['max_volumes'] = QSpinBox()
        self.gui_params['max_volumes'].setRange(0, 999)
        self.gui_params['reverse'] = QCheckBox()
        self.gui_params['one_thread'] = QCheckBox()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(destination_label, 1, 0, 1, 1)
        grid.addWidget(name_label, 2, 0, 1, 1)
        grid.addWidget(skip_volumes_label, 3, 0, 1, 1)
        grid.addWidget(max_volumes_label, 4, 0, 1, 1)
        grid.addWidget(reverse_label, 5, 0, 1, 1)
        grid.addWidget(one_thread_label, 5, 3, 1, 1)

        grid.addWidget(self.gui_params['destination'], 1, 2, 1, 3)
        grid.addWidget(self.gui_params['name'], 2, 2, 1, 3)
        grid.addWidget(self.gui_params['skip_volumes'], 3, 2, 1, 3)
        grid.addWidget(self.gui_params['max_volumes'], 4, 2, 1, 3)
        grid.addWidget(self.gui_params['reverse'], 5, 2, 1, 2)
        grid.addWidget(self.gui_params['one_thread'], 5, 4, 1, 1)

        return grid

    def get_uri_grid(self):

        uri_grid = QGridLayout()

        uri_label = QLabel('Url')
        uri_label.setMaximumWidth(20)
        uri = QLineEdit()
        uri_grid.addWidget(uri_label, 0, 0, 1, 1)
        uri_grid.addWidget(uri, 0, 1, 1, 15)

        manga_link = QLabel('<a href="http://yuru-yuri.sttv.me/#resources-list">MangaDownloader site</a>')
        manga_link.setOpenExternalLinks(True)
        manga_link.resize(manga_link.sizeHint())
        uri_grid.addWidget(manga_link, 0, 16, 1, 1)

        self.lang_btn = QPushButton(self._translate('lang'), self)
        self.lang_btn.clicked.connect(self.next_lang)
        self.lang_btn.setFlat(True)
        self.lang_btn.setStyleSheet('border: 1px solid #555; background-color: #8f8; padding: 2px')
        self.lang_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.lang_btn.setMaximumWidth(22)
        uri_grid.addWidget(self.lang_btn, 0, 17, 1, 1)

        return uri_grid

    def init_ui(self):
        globalGrid = QGridLayout()

        logGrid = self.get_base_grid()
        configGrid = self.get_config_grid()
        uriGrid = self.get_uri_grid()

        globalGrid.addLayout(uriGrid, 0, 0, 1, 8)
        globalGrid.addLayout(configGrid, 1, 0, 2, 3)
        globalGrid.addLayout(logGrid,    1, 3, 2, 5)

        self.setLayout(globalGrid)

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

    def _run_downloader(self):
        pass
