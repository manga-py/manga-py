
from PyQt5.Qt import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (
    QLabel, QLineEdit, QCheckBox, QGridLayout,
    QSpinBox, QTextEdit, QPushButton, QDialog,
    QFormLayout, QListWidget, QAbstractItemView
)


class Base:

    def __init__(self, parent):

        self.parent = parent


class MainForm(Base):

    def get_base_grid(self):

        self.parent.gui_params['log'] = QTextEdit()
        self.parent.gui_params['log'].setReadOnly(True)

        grid = QGridLayout()
        grid.setSpacing(10)

        btn = QPushButton('Run', self)
        btn.clicked.connect(self.parent._run_downloader)
        btn.resize(btn.sizeHint())

        grid.addWidget(self.parent.gui_params['log'], 0, 0)

        # self.parent.gui_params['log'].insertHtml('<span style="color:red">asdasd</span><br>')

        grid.addWidget(btn, 1, 0)

        return grid

    def get_config_grid(self):
        destination_label = QLabel(self.parent._translate('destination'))
        name_label = QLabel(self.parent._translate('name'))
        skip_volumes_label = QLabel(self.parent._translate('skip_volume'))
        max_volumes_label = QLabel(self.parent._translate('max_volume'))
        reverse_label = QLabel(self.parent._translate('reverse'))
        one_thread_label = QLabel(self.parent._translate('one_thread'))

        self.parent.gui_params['destination'] = QLineEdit()
        self.parent.gui_params['name'] = QLineEdit()
        self.parent.gui_params['skip_volumes'] = QSpinBox()
        self.parent.gui_params['skip_volumes'].setRange(0, 999)
        self.parent.gui_params['max_volumes'] = QSpinBox()
        self.parent.gui_params['max_volumes'].setRange(0, 999)
        self.parent.gui_params['reverse'] = QCheckBox()
        self.parent.gui_params['one_thread'] = QCheckBox()

        form = QFormLayout()
        form.setSpacing(10)

        form.addRow(destination_label, self.parent.gui_params['destination'])
        form.addRow(name_label, self.parent.gui_params['name'])
        form.addRow(skip_volumes_label, self.parent.gui_params['skip_volumes'])
        form.addRow(max_volumes_label, self.parent.gui_params['max_volumes'])
        form.addRow(reverse_label, self.parent.gui_params['reverse'])
        form.addRow(one_thread_label, self.parent.gui_params['one_thread'])

        return form

    def get_uri_grid(self):

        def test():
            def __(text):
                print(text)
                print(cb.selectedItems())
            q = QDialog(self)
            _l = QFormLayout()

            cb = QListWidget()
            cb.addItems(['variant1', 'variant2', 'variant3', 'variant4'])
            cb.setSelectionMode(QAbstractItemView.MultiSelection)

            cb.activated.connect(__)

            _l.addRow(QLabel('test'), cb)

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

        self.parent.lang_btn = QPushButton(self.parent._translate('lang'), self)
        # self.parent.lang_btn.clicked.connect(self.parent.next_lang)
        self.parent.lang_btn.clicked.connect(test)
        self.parent.lang_btn.setFlat(True)
        self.parent.lang_btn.setStyleSheet('border: 1px solid #555; background-color: #8f8; padding: 2px')
        self.parent.lang_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.parent.lang_btn.setMaximumWidth(22)
        uri_grid.addWidget(self.parent.lang_btn, 0, 17, 1, 1)

        return uri_grid
