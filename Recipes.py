import sys
import sqlite3
from PyQt5 import QtWidgets, QtCore

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


class RandomRecipe(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)


class CheckRecipe(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)


class FixedRecipe(QtWidgets.QWidget):
    def __init__(self, parent=None):
        self.connection = sqlite3.connect("Pokecraft_Database.db")
        QtWidgets.QWidget.__init__(self, parent)
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        self.item_type = QtWidgets.QComboBox()
        self.item_type.setMinimumWidth(200)
        self.item_type.addItems(["Сокровище", "Покеболл", "Усилитель"])
        self.item_type.currentIndexChanged.connect(self.update_names)
        self.item_name = QtWidgets.QComboBox()
        self.item_name.setMinimumWidth(200)
        self.update_names()
        self.components = []
        for _ in range(0, 4):
            label = QtWidgets.QLineEdit()
            label.setMaximumWidth(200)
            label.setReadOnly(True)
            self.components.append(label)
        grid = QtWidgets.QGridLayout()
        main_layout.addLayout(grid)
        grid.addWidget(QtWidgets.QLabel("Выберите тип предмета:"), 0, 0, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.item_type, 0, 1, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(QtWidgets.QLabel("Выберите название предмета:"), 1, 0, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.item_name, 1, 1, alignment=QtCore.Qt.AlignLeft)
        grid.addLayout(NamedLayout("Компонент 1:", self.components[0]), 2, 0, alignment=QtCore.Qt.AlignLeft)
        grid.addLayout(NamedLayout("Компонент 2:", self.components[1]), 2, 1, alignment=QtCore.Qt.AlignLeft)
        grid.addLayout(NamedLayout("Компонент 3:", self.components[2]), 3, 0, alignment=QtCore.Qt.AlignLeft)
        grid.addLayout(NamedLayout("Компонент 4:", self.components[3]), 3, 1, alignment=QtCore.Qt.AlignLeft)
        grid.setContentsMargins(10, 25, 10, 100)
        grid.setVerticalSpacing(20)

    def update_names(self):
        self.item_name.clear()
        with self.connection:
            item_type = self.item_type.currentText()
            cursor = self.connection.cursor()
            sql = f"SELECT name FROM Fixed_Recipes WHERE item_type = \"{item_type}\""
            cursor.execute(sql)
            for result in cursor.fetchall():
                self.item_name.addItem(*result)
        self.update()

    def update_recipe(self):
        with self.connection:
            name = self.item_name.currentText()
            cursor = self.connection.cursor()
            sql = f"SELECT component_1, component_2, component_3, component_4 FROM Fixed_Recipes " \
                  f"WHERE name = \"{name}\""
            cursor.execute(sql)
            result = cursor.fetchone()
            for index in range (0, 4):
                self.components[index].setReadOnly(False)
                self.components[index].setText(str(result[index]))
                self.components[index].setReadOnly(True)
        self.update()


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
        self.tabs.addTab(self.standart_recipe_type, "Стандартный")
        self.fixed_recipe_tab = FixedRecipe()
        self.tabs.addTab(self.fixed_recipe_tab, "Фиксированный")
        self.random_recipe = RandomRecipe()
        self.tabs.addTab(self.random_recipe, "Случайный")
        self.check_recipe_tab = CheckRecipe()
        self.tabs.addTab(self.check_recipe_tab, "Проверить результат")
        self.setLayout(main_layout)
        show_recipe = QtWidgets.QPushButton("Показать рецепт")
        show_recipe.clicked.connect(self.show_recipe)
        main_layout.addWidget(show_recipe)
        self.quit_button = QtWidgets.QPushButton("Выход")
        self.quit_button.clicked.connect(self.close)
        main_layout.addWidget(self.quit_button)

    def show_recipe(self):
        if self.tabs.currentIndex() == 1:
            self.fixed_recipe_tab.update_recipe()





app = QtWidgets.QApplication(sys.argv)
window = BaseWindow()
window.show()
sys.exit(app.exec_())
