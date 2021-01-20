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


class ResetableComponent(NamedLayout):
    def __init__(self, label, content, parent=None):
        NamedLayout.__init__(self, label=label, content=content, parent=parent)
        self.reset = QtWidgets.QPushButton("Изменить")
        self.addWidget(self.reset)


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
        self.use_unique = QtWidgets.QCheckBox()
        main_layout.addLayout(LongLabel("Использовать уникальные предметы", self.use_unique))
        self.item_type = QtWidgets.QComboBox()
        self.item_type.addItem("Любой")
        self.item_type.addItems(type_list)
        main_layout.addLayout(LongLabel("Выберите тип предмета:", self.item_type))
        self.min_price = QtWidgets.QSpinBox()
        self.min_price.setMaximum(9999)
        self.min_price.valueChanged.connect(self.check_max_price)
        self.max_price = QtWidgets.QSpinBox()
        self.max_price.setMaximum(10000)
        self.max_price.valueChanged.connect(self.check_min_price)
        main_layout.addLayout(LongLabel("Минимальная цена ингридиентов:", self.min_price))
        main_layout.addLayout(LongLabel("Максимальная цена ингридиентов:", self.max_price))
        self.part1 = QtWidgets.QComboBox()
        self.part2 = QtWidgets.QComboBox()
        self.part3 = QtWidgets.QComboBox()
        self.part4 = QtWidgets.QComboBox()
        self.result = QtWidgets.QLineEdit()
        self.result.setReadOnly(True)
        self.result.setMinimumWidth(300)
        self.result.setMaximumWidth(300)
        grid = QtWidgets.QGridLayout()
        grid.addLayout(ResetableComponent("Компонент 1", self.part1), 0, 0)
        grid.addLayout(ResetableComponent("Компонент 2", self.part2), 0, 1)
        grid.addLayout(ResetableComponent("Компонент 3", self.part3), 1, 0)
        grid.addLayout(ResetableComponent("Компонент 4", self.part4), 1, 1)
        grid.addLayout(NamedLayout("Результат:", self.result), 2, 0, 1, 2, QtCore.Qt.AlignHCenter)
        grid.setHorizontalSpacing(25)
        grid.setContentsMargins(5, 5, 5, 10)
        main_layout.addLayout(grid)

    def check_max_price(self):
        if int(self.min_price.value()) > 0:
            if self.min_price.value() == self.max_price.value():
                self.max_price.setValue(self.max_price.value()+1)

    def check_min_price(self):
        if int(self.min_price.value()) > 0:
            if self.min_price.value() == self.max_price.value():
                self.min_price.setValue(self.max_price.value()-1)


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
