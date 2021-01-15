import sys
import sqlite3
from PyQt5 import QtWidgets

type_list = ("Нормальный", "Боевой", "Летающий", "Ядовитый", "Земляной", "Каменный", "Насекомый", "Призрачный",
             "Стальной", "Огненный", "Водный", "Травяной", "Электрический", "Психический", "Ледяной", "Драконий",
             "Тёмный", "Волшебный")


class LongLabel(QtWidgets.QHBoxLayout):
    def __init__(self, label, content, parent=None):
        QtWidgets.QHBoxLayout.__init__(self, parent)
        label = QtWidgets.QLabel(label)
        label.setMinimumWidth(300)
        self.addWidget(label)
        if isinstance(content, QtWidgets.QVBoxLayout) or isinstance(content, QtWidgets.QHBoxLayout):
            self.addLayout(content)
        else:
            self.addWidget(content)


class StandartRecipe(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        self.use_uniques = QtWidgets.QCheckBox()
        main_layout.addLayout(LongLabel("Использовать уникальные предметы", self.use_uniques))
        self.minimum_sell_price = QtWidgets.QSpinBox()
        self.maximum_sell_price = QtWidgets.QSpinBox()
        price_container = QtWidgets
        grid = QtWidgets.QGridLayout()
        main_layout.addLayout(grid)





class BaseWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.resize(550, 450)
        self.setWindowTitle("Выбор рецепта Крам-о-Матика")
        main_layout = QtWidgets.QVBoxLayout()
        self.tabs = QtWidgets.QTabWidget()
        main_layout.addWidget(self.tabs)
