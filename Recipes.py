import sys
import sqlite3
from PyQt5 import QtWidgets, QtCore
from random import choice

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
        self.connection = sqlite3.connect("Pokecraft_Database.db")
        QtWidgets.QWidget.__init__(self, parent)
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        self.use_unique = QtWidgets.QCheckBox()
        main_layout.addLayout(LongLabel("Использовать уникальные предметы", self.use_unique))
        self.item_type = QtWidgets.QComboBox()
        self.item_type.addItem("Любой")
        self.item_type.addItems(type_list)
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
            if item_type not in type_list:
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
                print(total_value)
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
            item_type.addItems(type_list)
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
        self.item_type.addItems(type_list)
        self.item_type.currentIndexChanged.connect(self.update_item_list)
        main_layout.addLayout(LongLabel("Выберите тип предмета:", self.item_type))
        self.item_name = QtWidgets.QComboBox()
        with self.connection:
            item_type = self.item_type.currentText()
            cursor = self.connection.cursor()
            sql = f"SELECT name FROM Fixed_Recipes WHERE item_type = \"{item_type}\" ORDER BY name ASC"
            cursor.execute(sql)
            for result in cursor.fetchall():
                self.item_name.addItem(*result)
        main_layout.addLayout(LongLabel("Выберите название предмета:", self.item_name))
        self.min_price = QtWidgets.QSpinBox()
        self.min_price.setMaximum(9999)
        self.min_price.valueChanged.connect(self.check_max_price)
        self.max_price = QtWidgets.QSpinBox()
        self.max_price.setMaximum(10000)
        self.max_price.valueChanged.connect(self.check_min_price)
        main_layout.addLayout(LongLabel("Минимальная цена ингридиентов:", self.min_price))
        main_layout.addLayout(LongLabel("Максимальная цена ингридиентов:", self.max_price))
        grid = QtWidgets.QGridLayout()
        main_layout.addLayout(grid)
        self.first_part = QtWidgets.QLabel()
        self.second_part = QtWidgets.QLabel()
        self.third_part = QtWidgets.QLabel()
        self.fourth_part = QtWidgets.QLabel()
        grid.addLayout(ResetableComponent("Первый ингридиент:", self.first_part), 0, 0)
        grid.addLayout(ResetableComponent("Второй ингридиент:", self.second_part), 0, 1)
        grid.addLayout(ResetableComponent("Третий ингридиент:", self.third_part), 1, 0)
        grid.addLayout(ResetableComponent("Четвёртый ингридиент:", self.fourth_part), 1, 1)

    def check_min_price(self):
        if int(self.min_price.value()) > 0:
            if self.min_price.value() == self.max_price.value():
                self.min_price.setValue(self.max_price.value() - 1)

    def check_max_price(self):
        if int(self.min_price.value()) > 0:
            if self.min_price.value() == self.max_price.value():
                self.max_price.setValue(self.max_price.value() + 1)

    def update_item_list(self):
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
            cursor = self.connection.cursor()
            name = self.item_name.currentText()
            item_type = self.item_type.currentText()
            use_uniques = self.use_uniques.checkState()
            if use_uniques == 2:
                use_uniques = 1
            sql = f"SELECT min_value FROM Products WHERE name = \"{name}\""
            cursor.execute(sql)
            min_value = int(*cursor.fetchone())
            sql = f"SELECT max_value FROM Products WHERE name = \"{name}\""
            cursor.execute(sql)
            max_value = int(*cursor.fetchone())
            sql = f"SELECT name FROM Materials WHERE item_type = \"{item_type}\" AND is_unique = {use_uniques}"
            cursor.execute(sql)
            component1 = choice(self.result_list(cursor.fetchall()))

        self.update()

    def result_list(self, sql_result):
        list = []
        for result in sql_result:
            list.append(*result)
        return list


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


app = QtWidgets.QApplication(sys.argv)
window = BaseWindow()
window.show()
sys.exit(app.exec_())
