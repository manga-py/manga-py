from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QCheckBox, QGridLayout,
    QDesktopWidget, QMessageBox, QSpinBox, QTextEdit,
    QPushButton, QDialog, QFormLayout, QComboBox
)
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.Qt import Qt
from .CheckableComboBox import CheckableComboBox
from argparse import ArgumentParser
from libs.gui import config_storage
from libs.cli import Parser


class Gui(QWidget):  # pragma: no cover

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
        self.parser.set_quest_callback(self.quest)
        self.config_storage = config_storage.ConfigStorage()

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

    def get_base_grid(self):

        self.gui_params['log'] = QTextEdit()
        self.gui_params['log'].setReadOnly(True)

        grid = QGridLayout()
        grid.setSpacing(10)

        btn = QPushButton('Run', self)
        btn.clicked.connect(self._run_downloader)
        btn.resize(btn.sizeHint())

        grid.addWidget(self.gui_params['log'], 0, 0)

        # self.gui_params['log'].insertHtml('<span style="color:red">asdasd</span><br>')

        grid.addWidget(btn, 1, 0)

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

        form = QFormLayout()
        form.setSpacing(10)

        form.addRow(destination_label, self.gui_params['destination'])
        form.addRow(name_label, self.gui_params['name'])
        form.addRow(skip_volumes_label, self.gui_params['skip_volumes'])
        form.addRow(max_volumes_label, self.gui_params['max_volumes'])
        form.addRow(reverse_label, self.gui_params['reverse'])
        form.addRow(one_thread_label, self.gui_params['one_thread'])

        return form

    def get_uri_grid(self):

        def test():
            def __(text):
                print(text)
                q.setWindowTitle(str(text))
            q = QDialog(self)
            _l = QFormLayout()
            cb = QComboBox(self)
            cb.addItems(['variant1', 'variant2', 'variant3', 'variant4'])

            _cb = CheckableComboBox()
            _cb.addItems(['variant1', 'variant2', 'variant3', 'variant4'])

            cb.activated.connect(__)

            _l.addRow(QLabel('test'), cb)
            _l.addRow(QLabel('multi test'), _cb)

            q.setLayout(_l)
            q.open()

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
        # self.lang_btn.clicked.connect(test)
        self.lang_btn.setFlat(True)
        self.lang_btn.setStyleSheet('border: 1px solid #555; background-color: #8f8; padding: 2px')
        self.lang_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.lang_btn.setMaximumWidth(22)
        uri_grid.addWidget(self.lang_btn, 0, 17, 1, 1)

        return uri_grid

    def init_ui(self):
        global_grid = QGridLayout()
        _grid = QGridLayout()

        _grid.addLayout(self.get_config_grid(), 0, 0)
        _grid.addLayout(self.get_base_grid(),   0, 1)

        global_grid.addLayout(self.get_uri_grid(), 0, 0)
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
        pass
