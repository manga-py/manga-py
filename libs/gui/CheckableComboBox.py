from PyQt5.QtWidgets import QComboBox
from PyQt5.Qt import Qt


class CheckableComboBox(QComboBox):

    def flags(self, index):
        return Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled

