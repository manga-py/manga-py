#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QCheckBox,
     QDesktopWidget, QMessageBox, QSpinBox, QTextEdit, QGridLayout,
     QApplication, QPushButton)
from PyQt5.QtGui import QIcon


class Example(QWidget):

    window_h = 600
    window_w = 900
    in_work = False
    gui_params = {}

    def __init__(self):
        super().__init__()

        self.initUI()

    def getBaseGrid(self):

        log_label = QLabel('Log')
        self.gui_params['log'] = QTextEdit()
        self.gui_params['log'].setReadOnly(True)

        grid = QGridLayout()
        grid.setSpacing(10)

        btn = QPushButton('Run', self)
        btn.clicked.connect(self.center)
        btn.resize(btn.sizeHint())

        grid.addWidget(log_label, 1, 0, 5, 1)
        grid.addWidget(self.gui_params['log'], 1, 1, 5, 3)

        grid.addWidget(btn, 6, 3, 1, 1)

        return grid

    def getConfigGrid(self):
        destination_label = QLabel('Destination')
        name_label = QLabel('Name')
        skip_volumes_label = QLabel('Skip vol.')
        max_volumes_label = QLabel('Max vol.')
        reverse_label = QLabel('Reverse')

        self.gui_params['destination'] = QLineEdit()
        self.gui_params['name'] = QLineEdit()
        self.gui_params['skip_volumes'] = QSpinBox()
        self.gui_params['skip_volumes'].setRange(0, 999)
        self.gui_params['max_volumes'] = QSpinBox()
        self.gui_params['max_volumes'].setRange(0, 999)
        self.gui_params['reverse'] = QCheckBox()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(destination_label, 1, 0)
        grid.addWidget(self.gui_params['destination'], 1, 1)
        grid.addWidget(name_label, 2, 0)
        grid.addWidget(self.gui_params['name'], 2, 1)
        grid.addWidget(skip_volumes_label, 3, 0)
        grid.addWidget(self.gui_params['skip_volumes'], 3, 1)
        grid.addWidget(max_volumes_label, 4, 0)
        grid.addWidget(self.gui_params['max_volumes'], 4, 1)
        grid.addWidget(reverse_label, 5, 0)
        grid.addWidget(self.gui_params['reverse'], 5, 1)

        return grid

    def initUI(self):
        globalGrid = QGridLayout()

        logGrid = self.getBaseGrid()
        configGrid = self.getConfigGrid()
        uriGrid = QGridLayout()

        uri_label = QLabel('Url')
        uri = QLineEdit()
        uriGrid.addWidget(uri_label, 1, 0)
        uriGrid.addWidget(uri, 1, 1)

        globalGrid.addLayout(uriGrid, 0, 0, 1, 3)
        globalGrid.addLayout(logGrid, 1, 1, 2, 2)
        globalGrid.addLayout(configGrid, 1, 0, 2, 1)

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
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    ex.center()
    sys.exit(app.exec_())