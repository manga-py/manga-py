#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from os import path, makedirs
import json
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QCheckBox,
     QDesktopWidget, QMessageBox, QSpinBox, QTextEdit, QGridLayout,
     QApplication, QPushButton)
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.Qt import Qt
from pathlib import Path
import subprocess

# TODO: Need print messages to GUI from providers
# FIXME: Balumanga sources


class ConfigStorage:

    __config_path = ''
    __storage = {}
    __lang = {}

    def __init__(self):
        self.__config_path = path.join(str(Path.home()), 'AppData', 'Roaming', 'PyMangaDownloader', 'config.json')
        if not path.isfile(self.__config_path):
            self.__make_default_config()
        else:
            self.__load_config()
        self.__load_lang(self.__storage['lang'])

    def __load_json_config(self, f):
        return json.loads(''.join(f.readlines()))

    def __make_default_config(self):
        config_path = path.dirname(self.__config_path)
        path.isdir(config_path) or makedirs(config_path)
        with open(self.__config_path, 'w') as f:
            f.write(json.dumps({
                'lang': 'en',
            }))
        self.__storage['lang'] = 'en'
        self.__storage['url'] = ''

    def __load_config(self):
        with open(self.__config_path) as f:
            try:
                _json = self.__load_json_config(f)
            except json.JSONDecodeError:
                _json = {}
            self.__storage = _json
            self.__storage['lang'] = getattr(_json, 'lang', 'en')
            self.__storage['url'] = getattr(_json, 'lang', '')

    def __load_lang(self, key):
        _path = path.join(path.dirname(path.realpath(__file__)), 'helpers', '.gui.lang.{}.json')
        if not path.isfile(_path.format(key)):
            key = 'en'
        _path = _path.format(key)
        with open(_path) as f:
            self.__lang = self.__load_json_config(f)

    def get_param(self, key, default=None):
        """
        :param key: str
        :param default: str
        :return: mixed
        """
        return getattr(self, key, default)

    def set_param(self, key, value):
        self.__storage[key] = value

    def get_label(self, name):
        return self.get_param('label_{}'.format(name))

    def get_button(self, name):
        return self.get_param('button_{}'.format(name))

    def save_lang(self, key):
        pass

    def load_lang(self, key):
        pass

    def get_config(self):
        if hasattr(self.__storage, 'config'):
            return self.__storage['config']
        with open(self.__config_path) as f:
            config = self.__load_json_config(f)
            self.__storage['config'] = config['config']
            return config['config']

    def save_config(self):
        with open(self.__config_path, 'w') as f:
            f.write(json.dumps(self.__storage))


class GUI(QWidget):

    window_h = 600
    window_w = 900
    in_work = False
    gui_params = {}

    def __init__(self):
        super().__init__()

        self.init_ui()
        self.center()

    def get_base_grid(self):

        # log_label = QLabel('Log')
        self.gui_params['log'] = QTextEdit()
        self.gui_params['log'].setReadOnly(True)

        grid = QGridLayout()
        grid.setSpacing(10)

        btn = QPushButton('Run', self)
        btn.clicked.connect(self._run_downloader)
        btn.resize(btn.sizeHint())

        # grid.addWidget(log_label, 1, 0, 5, 1)
        grid.addWidget(self.gui_params['log'], 0, 0, 5, 3)

        # self.gui_params['log'].insertHtml('<span style="color:blue">asdasd</span><br>')
        # self.gui_params['log'].insertHtml('<span style="color:blue">asdasd</span><br>')
        # self.gui_params['log'].insertHtml('<span style="color:red">asdasd</span><br>')
        # self.gui_params['log'].insertHtml('<span style="color:blue">asdasd</span><br>')

        grid.addWidget(btn, 6, 1, 1, 1)

        return grid

    def get_config_grid(self):
        destination_label = QLabel('Destination')
        name_label = QLabel('Name')
        skip_volumes_label = QLabel('Skip vol.')
        max_volumes_label = QLabel('Max vol.')
        reverse_label = QLabel('Reverse')
        one_thread_label = QLabel('One thread')

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

        uriGrid = QGridLayout()

        uri_label = QLabel('Url')
        uri_label.setMaximumWidth(20)
        uri = QLineEdit()
        uriGrid.addWidget(uri_label, 0, 0, 1, 1)
        uriGrid.addWidget(uri, 0, 1, 1, 15)

        manga_link = QLabel('<a href="http://yuru-yuri.sttv.me/#resources-list">MangaDownloader site</a>')
        manga_link.setOpenExternalLinks(True)
        manga_link.resize(manga_link.sizeHint())
        uriGrid.addWidget(manga_link, 0, 16, 1, 1)

        lang_btn = QPushButton('en', self)
        lang_btn.setFlat(True)
        lang_btn.setStyleSheet('border: 1px solid #555; background-color: #8f8; padding: 2px')
        lang_btn.setCursor(QCursor(Qt.PointingHandCursor))
        lang_btn.setMaximumWidth(22)
        uriGrid.addWidget(lang_btn, 0, 17, 1, 1)

        return uriGrid

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
        self.show()

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

    def _add_to_log(self, text, *args, **kwargs):
        pass

    @staticmethod
    def _params_builder():
        return [
            ''
        ]

    def _run_downloader(self):
        params = self._params_builder()
        _dir = path.join(path.dirname(path.realpath(__file__)))
        subprocess.call(('{}/manga.exe {}'.format(_dir, ' '.join(params))), stdout=self._add_to_log)
        pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui_storage = ConfigStorage()
    gui_widget = GUI()
    sys.exit(app.exec_())
