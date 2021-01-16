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


class NamedLayout(QtWidgets.QVBoxLayout):
    def __init__(self, label, content, parent=None):
        QtWidgets.QVBoxLayout.__init__(self, parent)
        label = QtWidgets.QLabel(label)
        self.addWidget(label)
        self.addWidget(content)


class EditItemName(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)


class FixedRecipe(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        self.item_type = QtWidgets.QComboBox()
        self.item_type.addItems(["Сокровище", "Покеболл", "Усилитель"])
        main_layout.addLayout(LongLabel("Выберите тип предмета:", self.item_type))


class StandartRecipe(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        self.use_uniques = QtWidgets.QCheckBox()
        main_layout.addLayout(LongLabel("Использовать уникальные предметы", self.use_uniques))
        self.minimum_sell_price = QtWidgets.QSpinBox()
        self.minimum_sell_price.setMaximum(999999)
        self.minimum_sell_price.valueChanged.connect(self.check_maximum)
        self.maximum_sell_price = QtWidgets.QSpinBox()
        self.maximum_sell_price.setMaximum(999999)
        self.maximum_sell_price.valueChanged.connect(self.check_minimum)
        price_container = QtWidgets.QVBoxLayout()
        price_container.addWidget(QtWidgets.QLabel("От:"))
        price_container.addWidget(self.minimum_sell_price)
        price_container.addWidget(QtWidgets.QLabel("До:"))
        price_container.addWidget(self.maximum_sell_price)
        main_layout.addLayout(LongLabel("Цена ингридиетов", price_container))
        self.item_type = QtWidgets.QComboBox()
        self.item_type.addItems(type_list)
        main_layout.addLayout(LongLabel("Тип предмета", self.item_type))
        grid = QtWidgets.QGridLayout()
        main_layout.addLayout(grid)
        self.first_part = QtWidgets.QLabel()
        self.second_part = QtWidgets.QLabel()
        self.third_part = QtWidgets.QLabel()
        self.fourth_part = QtWidgets.QLabel()
        grid.addLayout(NamedLayout("Первый ингридиент:", self.first_part), 0, 0)
        grid.addLayout(NamedLayout("Второй ингридиент:", self.second_part), 0, 1)
        grid.addLayout(NamedLayout("Третий ингридиент:", self.third_part), 1, 0)
        grid.addLayout(NamedLayout("Четвёртый ингридиент:", self.fourth_part), 1, 1)


    def check_minimum(self):
        if self.maximum_sell_price.value() == self.minimum_sell_price.value():
            self.minimum_sell_price.setValue(int(self.minimum_sell_price.value())-1)

    def check_maximum(self):
        if self.maximum_sell_price.value() == self.minimum_sell_price.value():
            self.maximum_sell_price.setValue(int(self.maximum_sell_price.value())+1)




class BaseWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.resize(700, 550)
        self.setWindowTitle("Выбор рецепта Крам-о-Матика")
        main_layout = QtWidgets.QVBoxLayout()
        self.tabs = QtWidgets.QTabWidget()
        main_layout.addWidget(self.tabs)
        self.standart_recipe_type = StandartRecipe()
        self.tabs.addTab(self.standart_recipe_type, "Стандартный рецепт")
        self.fixed_recipe_tab = FixedRecipe()
        self.tabs.addTab(self.fixed_recipe_tab, "Фиксированный рецепт")
        self.edit_item_name = EditItemName()
        self.tabs.addTab(self.edit_item_name,"Редактировать название предметов")
        self.setLayout(main_layout)
        self.show_recipe = QtWidgets.QPushButton("Показать рецепт")
        main_layout.addWidget(self.show_recipe)
        self.quit_button = QtWidgets.QPushButton("Выход")
        self.quit_button.clicked.connect(self.close)
        main_layout.addWidget(self.quit_button)


app = QtWidgets.QApplication(sys.argv)
window = BaseWindow()
window.show()
sys.exit(app.exec_())
