import sys
import sqlite3
from PyQt5 import QtWidgets, QtCore
from random import choice

_type_list = ("Нормальный", "Боевой", "Летающий", "Ядовитый", "Земляной", "Каменный", "Насекомый", "Призрачный",
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
        self.connection = sqlite3.connect("Pokecraft_Database.db")
        QtWidgets.QWidget.__init__(self, parent)
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        self.use_unique = QtWidgets.QCheckBox()
        main_layout.addLayout(LongLabel("Использовать уникальные предметы", self.use_unique))
        self.item_type = QtWidgets.QComboBox()
        self.item_type.addItem("Любой")
        self.item_type.addItems(_type_list)
        main_layout.addLayout(LongLabel("Выберите тип предмета:", self.item_type))
        self.min_price = QtWidgets.QComboBox()
        self.min_price.currentIndexChanged.connect(self.check_max_price)
        self.max_price = QtWidgets.QComboBox()
        self.set_prices()
        self.max_price.currentIndexChanged.connect(self.check_min_price)
        main_layout.addLayout(LongLabel("Минимальная цена компонентов:", self.min_price))
        main_layout.addLayout(LongLabel("Максимальная цена компонентов:", self.max_price))
        self.components = []
        self.resets = []
        for index in range(1, 5):
            label = QtWidgets.QLineEdit()
            label.setMaximumWidth(200)
            label.setReadOnly(True)
            self.components.append(label)
            reset = ResetableComponent(f"Компонент {index}", label)
            self.resets.append(reset)
        self.resets[0].reset.clicked.connect(lambda: self.component_reroll(0))
        self.resets[1].reset.clicked.connect(lambda: self.component_reroll(1))
        self.resets[2].reset.clicked.connect(lambda: self.component_reroll(2))
        self.resets[3].reset.clicked.connect(lambda: self.component_reroll(3))
        self.result = QtWidgets.QLineEdit()
        self.result.setReadOnly(True)
        self.result.setMinimumWidth(300)
        self.result.setMaximumWidth(300)
        grid = QtWidgets.QGridLayout()
        main_layout.addLayout(grid)
        grid.addLayout(self.resets[0], 0, 0, alignment=QtCore.Qt.AlignLeft)
        grid.addLayout(self.resets[1], 0, 1, alignment=QtCore.Qt.AlignLeft)
        grid.addLayout(self.resets[2], 1, 0, alignment=QtCore.Qt.AlignLeft)
        grid.addLayout(self.resets[3], 1, 1, alignment=QtCore.Qt.AlignLeft)
        grid.addLayout(NamedLayout("Результат:", self.result), 2, 0, 1, 2, QtCore.Qt.AlignHCenter)
        grid.setHorizontalSpacing(25)
        grid.setContentsMargins(5, 5, 5, 10)

    def set_prices(self):
        for price in range(0, 2001, 100):
            self.min_price.addItem(str(price))
            self.max_price.addItem(str(price))
        for price in range(3000, 10001, 1000):
            self.min_price.addItem(str(price))
            self.max_price.addItem(str(price))
        price = 20000
        self.min_price.addItem(str(price))
        self.max_price.addItem(str(price))
        self.max_price.setCurrentText(str(price))

    def check_max_price(self):
        if self.min_price.currentText() == "20000":
            self.max_price.setCurrentText("20000")
            self.update_all_names()
        elif self.min_price.currentIndex() > self.max_price.currentIndex():
            if self.min_price.currentIndex() > 0:
                step = self.max_price.currentIndex() + 1
                self.max_price.setCurrentIndex(step)
                self.update_all_names()

    def check_min_price(self):
        if self.max_price.currentText() == "0":
            self.min_price.setCurrentText("0")
            self.update_all_names()
        elif self.min_price.currentIndex() > self.max_price.currentIndex():
            if self.max_price.currentText() != "20000":
                step = self.max_price.currentIndex() - 1
                self.min_price.setCurrentIndex(step)
                self.update_all_names()

    def update_all_names(self):
        for index in range(4):
            self.update_names(index)
            self.update()

    def update_recipe(self):
        with self.connection:
            cursor = self.connection.cursor()
            item_type = self.item_type.currentText()
            if item_type not in _type_list:
                if self.use_unique.checkState() != 0:
                    sql = "SELECT name, value, item_type FROM Materials"
                else:
                    sql = "SELECT name, value, item_type FROM Materials WHERE is_unique = 0"
                cursor.execute(sql)
                material1 = choice(cursor.fetchall())
                item_type = material1[2]
            else:
                if self.use_unique.checkState() != 0:
                    sql = f"SELECT name, value FROM Materials WHERE item_type = \"{item_type}\""
                else:
                    sql = f"SELECT name, value FROM Materials WHERE item_type = \"{item_type}\" " \
                          "AND is_unique = 0"
                cursor.execute(sql)
                material1 = choice(cursor.fetchall())
            if self.use_unique.checkState() != 0:
                sql = "SELECT name, value FROM Materials"
            else:
                sql = "SELECT name, value FROM Materials WHERE is_unique = 0"
            cursor.execute(sql)
            result = cursor.fetchall()
            materials = [material1]
            for _ in range(3):
                material = choice(result)
                materials.append(material)
            value = 0
            for material in materials:
                value += material[1]
            sql = f"SELECT name FROM Products WHERE item_type = \"{item_type}\" AND min_value <= {value} AND max_value >= {value}"
            cursor.execute(sql)
            result = choice(cursor.fetchall())
            self.result.setReadOnly(False)
            self.result.setText(*result)
            self.result.setReadOnly(True)
            for index in range(4):
                self.components[index].setReadOnly(False)
                self.components[index].setText(materials[index][0])
                self.components[index].setReadOnly(True)
        self.update()

    def component_reroll(self, index):
        result_name = self.result.text()
        if len(result_name) > 3:
            min_price = int(self.min_price.currentText())
            max_price = int(self.max_price.currentText())
            with self.connection:
                cursor = self.connection.cursor()
                values = []
                for material in range(4):
                    name = self.components[material].text()
                    if material == 0 and index == 0:
                        sql = f"SELECT value, item_type FROM Materials WHERE name = \"{name}\""
                        cursor.execute(sql)
                        value, item_type = cursor.fetchone()
                    else:
                        sql = f"SELECT value FROM Materials WHERE name = \"{name}\""
                        cursor.execute(sql)
                        value = int(*cursor.fetchone())
                    if material == index:
                        material_value = value
                    values.append(value)
                total_value = sum(values)
                if total_value % 10 == 0:
                    if material_value >= 10:
                        min_value = (material_value // 10 - 1) * 10 + 1
                    else:
                        min_value = material_value // 10 * 10 + 1
                else:
                    min_value = material_value - total_value % 10 + 1
                max_value = min_value + 9
                if index == 0:
                    if self.use_unique.checkState() != 0:
                        sql = f"SELECT name FROM Materials WHERE item_type = \"{item_type}\" AND value >= {min_value} " \
                              f"AND value <= {max_value} AND sell_price >= {min_price} AND sell_price <= {max_price}"
                    else:
                        sql = f"SELECT name FROM Materials WHERE item_type = \"{item_type}\" AND value >= {min_value} " \
                              f"AND value <= {max_value} AND sell_price >= {min_price} AND sell_price <= {max_price} " \
                              f"AND is_unique = 0"
                else:
                    if self.use_unique.checkState() != 0:
                        sql = f"SELECT name FROM Materials WHERE value >= {min_value} AND value <= {max_value} " \
                              f"AND sell_price >= {min_price} AND sell_price <= {max_price}"
                    else:
                        sql = f"SELECT name FROM Materials WHERE value >= {min_value} AND value <= {max_value} " \
                              f"AND sell_price >= {min_price} AND sell_price <= {max_price} " \
                              f"AND is_unique = 0"
                cursor.execute(sql)
                try:
                    result = choice(cursor.fetchall())
                except:
                    return
                self.components[index].setReadOnly(False)
                self.components[index].setText(str(*result))
                self.components[index].setReadOnly(True)
            self.update()



class CheckRecipe(QtWidgets.QWidget):
    def __init__(self, parent=None):
        self.connection = sqlite3.connect("Pokecraft_Database.db")
        QtWidgets.QWidget.__init__(self, parent)
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        self.use_unique = QtWidgets.QCheckBox()
        self.use_unique.stateChanged.connect(self.update_all_names)
        main_layout.addLayout(LongLabel("Использовать уникальные предметы", self.use_unique))
        self.items_type = []
        self.components = []
        for index in range(1, 5):
            item_type = QtWidgets.QComboBox()
            item_type.addItem("Любой")
            item_type.addItems(_type_list)
            self.items_type.append(item_type)
            main_layout.addLayout(LongLabel(f"Выберите тип компонента {index}:", item_type))
        self.min_price = QtWidgets.QComboBox()
        self.min_price.currentIndexChanged.connect(self.check_max_price)
        self.max_price = QtWidgets.QComboBox()
        self.set_prices()
        self.max_price.currentIndexChanged.connect(self.check_min_price)
        main_layout.addLayout(LongLabel("Минимальная цена компонентов:", self.min_price))
        main_layout.addLayout(LongLabel("Максимальная цена компонентов:", self.max_price))
        for _ in range(0, 4):
            name_list = QtWidgets.QComboBox()
            name_list.setMinimumWidth(250)
            self.components.append(name_list)
        self.items_type[0].currentIndexChanged.connect(lambda: self.update_names(0))
        self.items_type[1].currentIndexChanged.connect(lambda: self.update_names(1))
        self.items_type[2].currentIndexChanged.connect(lambda: self.update_names(2))
        self.items_type[3].currentIndexChanged.connect(lambda: self.update_names(3))
        for index in range(4):
            self.update_names(index)
        self.result = QtWidgets.QLineEdit()
        self.result.setReadOnly(True)
        self.result.setMinimumWidth(300)
        self.result.setMaximumWidth(300)
        grid = QtWidgets.QGridLayout()
        grid.addLayout(NamedLayout("Компонент 1:", self.components[0]), 0, 0, alignment=QtCore.Qt.AlignLeft)
        grid.addLayout(NamedLayout("Компонент 2:", self.components[1]), 0, 1, alignment=QtCore.Qt.AlignLeft)
        grid.addLayout(NamedLayout("Компонент 3:", self.components[2]), 1, 0, alignment=QtCore.Qt.AlignLeft)
        grid.addLayout(NamedLayout("Компонент 4:", self.components[3]), 1, 1, alignment=QtCore.Qt.AlignLeft)
        grid.addLayout(NamedLayout("Результат:", self.result), 2, 0, 1, 2, QtCore.Qt.AlignHCenter)
        grid.setHorizontalSpacing(25)
        grid.setContentsMargins(5, 5, 5, 10)
        main_layout.addLayout(grid)

    def set_prices(self):
        for price in range(0, 2001, 100):
            self.min_price.addItem(str(price))
            self.max_price.addItem(str(price))
        for price in range(3000, 10001, 1000):
            self.min_price.addItem(str(price))
            self.max_price.addItem(str(price))
        price = 20000
        self.min_price.addItem(str(price))
        self.max_price.addItem(str(price))
        self.max_price.setCurrentText(str(price))

    def check_max_price(self):
        if self.min_price.currentText() == "20000":
            self.max_price.setCurrentText("20000")
            self.update_all_names()
        elif self.min_price.currentIndex() > self.max_price.currentIndex():
            if self.min_price.currentIndex() > 0:
                step = self.max_price.currentIndex() + 1
                self.max_price.setCurrentIndex(step)
                self.update_all_names()

    def check_min_price(self):
        if self.max_price.currentText() == "0":
            self.min_price.setCurrentText("0")
            self.update_all_names()
        elif self.min_price.currentIndex() > self.max_price.currentIndex():
            if self.max_price.currentText() != "20000":
                step = self.max_price.currentIndex() - 1
                self.min_price.setCurrentIndex(step)
                self.update_all_names()

    def update_names(self, index):
        type_check = self.items_type[index]
        item_type = type_check.currentText()
        min_price = int(self.min_price.currentText())
        max_price = int(self.max_price.currentText())
        use_uniques = self.use_unique.checkState()
        self.components[index].clear()
        with self.connection:
            cursor = self.connection.cursor()
            if not item_type == "Любой":
                if use_uniques == 0:
                    sql = f"SELECT name FROM Materials WHERE item_type = \"{item_type}\" AND sell_price >= {min_price} " \
                          f"AND sell_price <= {max_price} AND is_unique = 0 ORDER BY name ASC"
                else:
                    sql = f"SELECT name FROM Materials WHERE item_type = \"{item_type}\" AND sell_price >= {min_price} " \
                          f"AND sell_price <= {max_price} ORDER BY name ASC"
            else:
                if use_uniques == 0:
                    sql = f"SELECT name FROM Materials WHERE sell_price >= {min_price} " \
                          f"AND sell_price <= {max_price} AND is_unique = 0 ORDER BY name ASC"
                else:
                    sql = f"SELECT name FROM Materials WHERE sell_price >= {min_price} " \
                          f"AND sell_price <= {max_price} ORDER BY name ASC"
            cursor.execute(sql)
        for result in cursor.fetchall():
            self.components[index].addItem(*result)
        self.update()

    def update_all_names(self):
        for index in range(4):
            self.update_names(index)
            self.update()

    def update_recipe(self):
        part1 = self.components[0].currentText()
        part2 = self.components[1].currentText()
        part3 = self.components[2].currentText()
        part4 = self.components[3].currentText()
        parts = [part1, part2, part3, part4]
        if any(len(part) == 0 for part in parts):
            return
        cursor = self.connection.cursor()
        if part1 == part3 == part4:
            sql = f"SELECT EXISTS (SELECT * FROM Fixed_Recipes WHERE component_1 = \"{part1}\" AND" \
                  f" component_3 = \"{part3}\" AND component_4 = \"{part4}\")"
            cursor.execute(sql)
            if 0 not in cursor.fetchone():
                sql = f"SELECT name FROM Fixed_Recipes WHERE component_1 = \"{part1}\""
                cursor.execute(sql)
                result = choice(cursor.fetchall())
                self.result.setReadOnly(False)
                self.result.setText(*result)
                self.result.setReadOnly(True)
                return
        sql = f"SELECT item_type FROM Materials WHERE name = \"{part1}\""
        cursor.execute(sql)
        item_type = str(*cursor.fetchone())
        value = 0
        for part in parts:
            sql = f"SELECT value FROM Materials WHERE name = \"{part}\""
            cursor.execute(sql)
            part_value = int(*cursor.fetchone())
            value += part_value
        sql = f"SELECT name FROM Products WHERE item_type = \"{item_type}\" AND min_value <= {value} " \
              f"AND {value} <= max_value"
        cursor.execute(sql)
        result = cursor.fetchone()
        self.result.setReadOnly(False)
        self.result.setText(*result)
        self.result.setReadOnly(True)
        self.update()


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
            sql = f"SELECT name FROM Fixed_Recipes WHERE item_type = \"{item_type}\" ORDER BY name ASC"
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
            for index in range(0, 4):
                self.components[index].setReadOnly(False)
                self.components[index].setText(str(result[index]))
                self.components[index].setReadOnly(True)
        self.update()


class StandartRecipe(QtWidgets.QWidget):
    def __init__(self, parent=None):
        self.connection = sqlite3.connect("Pokecraft_Database.db")
        QtWidgets.QWidget.__init__(self, parent)
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        self.use_uniques = QtWidgets.QCheckBox()
        main_layout.addLayout(LongLabel("Использовать уникальные предметы", self.use_uniques))
        self.item_type = QtWidgets.QComboBox()
        self.item_type.addItems(_type_list)
        self.item_type.currentIndexChanged.connect(self.update_item_list)
        main_layout.addLayout(LongLabel("Выберите тип предмета:", self.item_type))
        self.item_name = QtWidgets.QComboBox()
        main_layout.addLayout(LongLabel("Выберите название предмета", self.item_name))
        self.item_name.currentIndexChanged.connect(self.set_result_clear)
        self.min_price = QtWidgets.QComboBox()
        self.min_price.currentIndexChanged.connect(self.check_max_price)
        self.max_price = QtWidgets.QComboBox()
        self.set_prices()
        self.max_price.currentIndexChanged.connect(self.check_min_price)
        main_layout.addLayout(LongLabel("Минимальная цена компонентов:", self.min_price))
        main_layout.addLayout(LongLabel("Максимальная цена компонентов:", self.max_price))
        self.components = []
        self.resets = []
        for index in range(1, 5):
            label = QtWidgets.QLineEdit()
            label.setMaximumWidth(200)
            label.setReadOnly(True)
            self.components.append(label)
            reset = ResetableComponent(f"Компонент {index}", label)
            self.resets.append(reset)
        self.resets[0].reset.clicked.connect(lambda: self.component_reroll(0))
        self.resets[1].reset.clicked.connect(lambda: self.component_reroll(1))
        self.resets[2].reset.clicked.connect(lambda: self.component_reroll(2))
        self.resets[3].reset.clicked.connect(lambda: self.component_reroll(3))
        self.update_item_list()
        grid = QtWidgets.QGridLayout()
        main_layout.addLayout(grid)
        grid.addLayout(self.resets[0], 0, 0, alignment=QtCore.Qt.AlignLeft)
        grid.addLayout(self.resets[1], 0, 1, alignment=QtCore.Qt.AlignLeft)
        grid.addLayout(self.resets[2], 1, 0, alignment=QtCore.Qt.AlignLeft)
        grid.addLayout(self.resets[3], 1, 1, alignment=QtCore.Qt.AlignLeft)
        grid.setHorizontalSpacing(25)
        grid.setContentsMargins(5, 5, 5, 10)

    def set_prices(self):
        for price in range(0, 2001, 100):
            self.min_price.addItem(str(price))
            self.max_price.addItem(str(price))
        for price in range(3000, 10001, 1000):
            self.min_price.addItem(str(price))
            self.max_price.addItem(str(price))
        price = 20000
        self.min_price.addItem(str(price))
        self.max_price.addItem(str(price))
        self.max_price.setCurrentText(str(price))

    def check_max_price(self):
        if self.min_price.currentText() == "20000":
            self.max_price.setCurrentText("20000")
            self.update_all_names()
        elif self.min_price.currentIndex() > self.max_price.currentIndex():
            if self.min_price.currentIndex() > 0:
                step = self.max_price.currentIndex() + 1
                self.max_price.setCurrentIndex(step)
                self.update_all_names()

    def check_min_price(self):
        if self.max_price.currentText() == "0":
            self.min_price.setCurrentText("0")
            self.update_all_names()
        elif self.min_price.currentIndex() > self.max_price.currentIndex():
            if self.max_price.currentText() != "20000":
                step = self.max_price.currentIndex() - 1
                self.min_price.setCurrentIndex(step)
                self.update_all_names()

    def update_item_list(self):
        self.set_result_clear()
        self.item_name.clear()
        with self.connection:
            item_type = self.item_type.currentText()
            cursor = self.connection.cursor()
            sql = f"SELECT name FROM Products WHERE item_type = \"{item_type}\" ORDER BY min_value ASC"
            cursor.execute(sql)
            for result in cursor.fetchall():
                self.item_name.addItem(*result)
        self.update()

    def set_result_clear(self):
        for index in range(4):
            self.components[index].setReadOnly(False)
            self.components[index].clear()
            self.components[index].setReadOnly(True)
        self.update()

    def update_recipe(self):
        with self.connection:
            cursor = self.connection.cursor()
            name = self.item_name.currentText()
            item_type = self.item_type.currentText()
            min_price = int(self.min_price.currentText())
            max_price = int(self.max_price.currentText())
            use_unique = self.use_uniques.checkState()
            sql = f"SELECT max_value FROM Products WHERE name = \"{name}\""
            cursor.execute(sql)
            max_value = int(*cursor.fetchone())
            if use_unique == 0:
                sql = f"SELECT name, value FROM Materials WHERE item_type = \"{item_type}\" AND value <= {max_value} " \
                      f"AND is_unique = 0 AND {min_price} <= sell_price AND sell_price <= {max_price}"
            else:
                sql = f"SELECT name, value FROM Materials WHERE item_type = \"{item_type}\" AND value <= {max_value} " \
                      f"AND {min_price} <= sell_price AND sell_price <= {max_price}"
            cursor.execute(sql)
            try:
                component1 = choice(cursor.fetchall())
            except:
                self.show_request_error()
                return
            components = [component1[0]]
            max_value -= component1[1]
            for _ in range(3):
                if use_unique == 0:
                    sql = f"SELECT name, value FROM Materials WHERE value <= {max_value} AND is_unique = 0 " \
                          f"AND {min_price} <= sell_price AND sell_price <= {max_price}"
                else:
                    sql = f"SELECT name, value FROM Materials WHERE value <= {max_value} " \
                          f"AND {min_price} <= sell_price AND sell_price <= {max_price}"
                cursor.execute(sql)
                try:
                    component = choice(cursor.fetchall())
                except:
                    self.show_request_error()
                    return
                components.append(component[0])
                max_value -= component[1]
            for index in range(4):
                self.components[index].setReadOnly(False)
                self.components[index].setText(str(components[index]))
                self.components[index].setReadOnly(True)
        self.update()

    def show_request_error(self):
        for index in range(4):
            self.components[index].setReadOnly(False)
        self.components[0].setText("Такое")
        self.components[1].setText("Условие")
        self.components[2].setText("Выполнить")
        self.components[3].setText("Невозможно")
        for index in range(4):
            self.components[index].setReadOnly(True)

    def component_reroll(self, index):
        result_name = self.item_name.currentText()
        if len(result_name) > 3:
            min_price = int(self.min_price.currentText())
            max_price = int(self.max_price.currentText())
            with self.connection:
                cursor = self.connection.cursor()
                values = []
                for material in range(4):
                    name = self.components[material].text()
                    if material == 0 and index == 0:
                        sql = f"SELECT value, item_type FROM Materials WHERE name = \"{name}\""
                        cursor.execute(sql)
                        value, item_type = cursor.fetchone()
                    else:
                        sql = f"SELECT value FROM Materials WHERE name = \"{name}\""
                        cursor.execute(sql)
                        value = int(*cursor.fetchone())
                    if material == index:
                        material_value = value
                    values.append(value)
                total_value = sum(values)
                if total_value % 10 == 0:
                    if material_value >= 10:
                        min_value = (material_value // 10 - 1) * 10 + 1
                    else:
                        min_value = material_value // 10 * 10 + 1
                else:
                    min_value = material_value - total_value % 10 + 1
                max_value = min_value + 9
                if index == 0:
                    if self.use_uniques.checkState() != 0:
                        sql = f"SELECT name FROM Materials WHERE item_type = \"{item_type}\" AND value >= {min_value} " \
                              f"AND value <= {max_value} AND sell_price >= {min_price} AND sell_price <= {max_price}"
                    else:
                        sql = f"SELECT name FROM Materials WHERE item_type = \"{item_type}\" AND value >= {min_value} " \
                              f"AND value <= {max_value} AND sell_price >= {min_price} AND sell_price <= {max_price} " \
                              f"AND is_unique = 0"
                else:
                    if self.use_uniques.checkState() != 0:
                        sql = f"SELECT name FROM Materials WHERE value >= {min_value} AND value <= {max_value} " \
                              f"AND sell_price >= {min_price} AND sell_price <= {max_price}"
                    else:
                        sql = f"SELECT name FROM Materials WHERE value >= {min_value} AND value <= {max_value} " \
                              f"AND sell_price >= {min_price} AND sell_price <= {max_price} " \
                              f"AND is_unique = 0"
                cursor.execute(sql)
                try:
                    result = choice(cursor.fetchall())
                except:
                    return
                self.components[index].setReadOnly(False)
                self.components[index].setText(str(*result))
                self.components[index].setReadOnly(True)
            self.update()


class HelpTab(QtWidgets.QToolBox):
    def __init__(self, parent=None):
        QtWidgets.QToolBox.__init__(self, parent)
        windows_text = """Стандартный:
Позволяет найти рецепт заданного пользователем предмета.
В строке выбора названия предмета продукты синтеза располагаются по возрастанию
цены синтеза. Подробнее см. "Кнока "Изменить"".

Фиксированный:
Показывает фиксированные рецепты - то есть, те, где три одинаковых предмета дают один и 
тот же итог не зависимо от четвёртого.

Случаный:
Генерирует случайный рецепт на основе заданных пользователем условий.

Проверить рецепт:
Пользователь выбирает 4 предмета и может проверить, что получится, если их 
скомбинировать с помощью Крам-о-Матика."""
        self.addItem(QtWidgets.QLabel(windows_text), "Вкладки")
        type_and_price_text = """Тип предмента:
По классификации Крам-о-Матика все предметы-материалы относятся к одному из 
18 типов, стандартных для покемонов. Продукты синтеза определяются типом 
первого предмета, выбранного пользователем. Таким образом, продукты синтеза 
тоже можно разделить на 18 типов, хотя некоторые предметы (например, 
Pearl String) могут встречаться в нескольких типах продуктов синтеза.

Минимальная и максимальная цена компонентов:
Назначает минимальную и максимальную допустимую цену для материалов синтеза.
При нажатии на кнопку "Показать рецепт" выбираются материалы из одного и того же
ценового диапазона, однако во вкладках "Стандартный" и "Случайный" диапазон для
отдельных компонентов можно изменить. Для этого после получения рецепта
необходимо изменить ценовой диапазон и изменить отдельный компонент. Если надпись
в поле названия компонента не поменялась даже после нескольких нажатий на кнопку
"Изменить" - значит, изменение при данном ценовом диапазоне невозможно."""
        self.addItem(QtWidgets.QLabel(type_and_price_text), "Тип и цена")
        use_unique_text = """В Крам-о-Матике возможно использование некоторых уникальных предметов.
        
К ним относятся особые предметы для Сильвалли, а также для Зашиан и Замазенты.
Использовав эти предметы в Крам-о-Матике, вы больше никак не сможете их получить!

По умолчанию использование уникальных предметов в рецептах отключено.

Чтобы включить его, посставьте галочку в соответствующем поле нажатием мыши.

Выбор этой опции в одной из влкадок не влияет на остальные"""
        self.addItem(QtWidgets.QLabel(use_unique_text), "Использование уникальных предметов")
        show_recipe_text = """Кнопка "Показать рецепт" работает немного по-разному в зависимости от вкладки.
        
На вкладке "Стандратный" она предлагает один из вариантов создания запрошенного
пользователем рецепта. При повторном нажатии она отобразит другой случайно 
выбранный вариант. 

Обратите внимание, что некоторые предметы (Rare Candy, PP Up и др.) относятся
сразу к нескольких типам. Программа будет выбирать тип первого материала 
исходя из того, какой выбран тип у продукта синтеза.
Подробнее см. "Тип и цена".

На вкладке "Фиксированный" кнопка покажет единственный возможный рецепт для
выбранного предмета. Второй ингридиент всегда может быть любым.

На вкладке "Случайный" программа покажет четыре случайных компонента и 
итог синтеза. При повторном нажатии полностью сбрасывает и результат,
и компоненты. Если требуется изменить один компонент, нажмите 
соответствующую кнопку.

На вкладке "Проверить результат" программа покажет итог синтеза из
выбранных пользователем четырёх компонентов.

На текущей вкладке кнопка не работает :)
"""
        self.addItem(QtWidgets.QLabel(show_recipe_text), "Кнопка \"Показать рецепт\"")
        reroll_text = """Во вкладках "Стандартный" и "Случайный" после выбора рецепта отдельные компоненты
можно изменить.

Это возможно потому, что каждый продукт синтеза в Крам-о-Матике, за исключением 
покеболллов, может быть создан несколькими способами. Каждый материал синтеза 
имеет свою "цену", и их сумма, наряду с типом первого материала в списке, 
определяет итог синтеза.

При нажатии на кнопку "Изменить" для первого компонента программа попытается 
подобрать материал с тем же типом и ценностью в таком диапазоне, чтобы итог с 
учётом остальных материалов остался тем же. 

При нажатии на кнопку "Изменить" для прочих компонентов в расчёт будет браться только
цена материала.

Если при многократном (4-5 раз) нажатии на кнопку "Изменить" ничего не происходит, 
значит, изменить рецепт с учётом текущих условий невозможно. Можно попробовать 
изменить ценовой диапазон для материалов (подробнее см. "Тип и цена") 

Если получившийся набор компонентов во вкладке "Стандартные" не устраивает 
категорически, проще нажать на кнопку "Показать рецепт" ещё раз, чем 
перебрасывать ингридиенты по одному, так как их значения связаны 
друг с другом."""
        self.addItem(QtWidgets.QLabel(reroll_text), "Кнопка \"Изменить\"")




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
        self.random_recipe_tab = RandomRecipe()
        self.tabs.addTab(self.random_recipe_tab, "Случайный")
        self.check_recipe_tab = CheckRecipe()
        self.tabs.addTab(self.check_recipe_tab, "Проверить результат")
        help = HelpTab()
        self.tabs.addTab(help, "Справка")
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
        elif self.tabs.currentIndex() == 3:
            self.check_recipe_tab.update_recipe()
        elif self.tabs.currentIndex() == 2:
            self.random_recipe_tab.update_recipe()
        else:
            self.standart_recipe_type.update_recipe()


app = QtWidgets.QApplication(sys.argv)
window = BaseWindow()
window.show()
sys.exit(app.exec_())
