import sys
import sqlite3
from PyQt5 import QtWidgets

type_list = ("Нормальный", "Боевой", "Летающий", "Ядовитый", "Земляной", "Каменный", "Насекомый", "Призрачный",
             "Стальной", "Огненный", "Водный", "Травяной", "Электрический", "Психический", "Ледяной", "Драконий",
             "Тёмный", "Волшебный")


class ItemExistsWindow(QtWidgets.QDialog):
    def __init__(self, parent, double_type):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Существующий предмет")
        main_layout = QtWidgets.QVBoxLayout()
        if double_type == "name":
            text = QtWidgets.QLabel("""Предмет с таким названием уже есть в базе данных.
Обновить данные?""")
        else:
            text = QtWidgets.QLabel("""Предмет с такой ценностью уже есть в базе данных.
Обновить данные?""")
        main_layout.addWidget(text)
        buttons_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(buttons_layout)
        self.button_accept = QtWidgets.QPushButton("Да")
        self.button_deny = QtWidgets.QPushButton("Нет")
        self.button_accept.clicked.connect(self.accept)
        self.button_deny.clicked.connect(self.deny)
        buttons_layout.addWidget(self.button_deny)
        buttons_layout.addWidget(self.button_accept)
        self.setLayout(main_layout)
        self.update = False

    def accept(self):
        self.setParent(None)
        self.hide()
        self.update = True

    def deny(self):
        self.setParent(None)
        self.hide()


class NamedWidget(QtWidgets.QVBoxLayout):
    def __init__(self, title, content, parent=None):
        QtWidgets.QVBoxLayout.__init__(self, parent)
        title = QtWidgets.QLabel(str(title))
        self.addWidget(title)
        if isinstance(content, QtWidgets.QVBoxLayout):
            self.addLayout(content)
        else:
            self.addWidget(content)


class ForCraftLayout(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(20)
        head = QtWidgets.QHBoxLayout()
        head.addWidget(QtWidgets.QLabel("Уникальный предмет"))
        self.unique = QtWidgets.QCheckBox()
        head.addWidget(self.unique)
        head.insertSpacing(1, 40)
        megahead = QtWidgets.QVBoxLayout()
        megahead.addLayout(head)
        megahead.insertSpacing(0, 15)
        self.grid.addLayout(megahead, 0, 0, 1, 2)
        self.name = QtWidgets.QLineEdit()
        self.grid.addLayout(NamedWidget(title="Название предмета:", content=self.name), 2, 0)
        self.item_type = QtWidgets.QComboBox()
        self.item_type.addItems(type_list)
        self.grid.addLayout(NamedWidget(title="Тип предмета:", content=self.item_type), 2, 1)
        self.value = QtWidgets.QSpinBox()
        self.value.setMinimum(0)
        self.grid.addLayout(NamedWidget(title="Ценность предмета:", content=self.value), 3, 0)
        self.price = QtWidgets.QSpinBox()
        self.price.setMinimum(0)
        self.price.setMaximum(999999)
        self.grid.addLayout(NamedWidget(title="Цена при продаже в магазине:", content=self.price), 3, 1)
        self.setLayout(self.grid)

    def reset(self):
        self.name.clear()
        self.value.setValue(0)
        self.price.setValue(0)
        self.unique.setCheckState(0)


class MayBeCraftedLayout(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(20)
        self.name = QtWidgets.QLineEdit()
        self.grid.addLayout(NamedWidget(title="Название предмета:", content=self.name), 0, 0)
        self.item_type = QtWidgets.QComboBox()
        self.item_type.addItems(type_list)
        self.grid.addLayout(NamedWidget(title="Тип предмета:", content=self.item_type), 0, 1)
        self.min_value = QtWidgets.QSpinBox()
        self.min_value.setMinimum(1)
        self.min_value.setMaximum(151)
        self.min_value.valueChanged.connect(self.change_maximum)
        self.max_value = QtWidgets.QSpinBox()
        self.max_value.setValue(20)
        self.max_value.valueChanged.connect(self.change_minimum)
        self.max_value.setMaximum(160)
        self.max_value.setMinimum(0)
        self.grid.addLayout(NamedWidget(title="Минимум очков для создания:", content=self.min_value), 1, 0)
        self.grid.addLayout(NamedWidget(title="Максимум очков для создания:", content=self.max_value), 1, 1)
        self.setLayout(self.grid)

    def change_maximum(self):
        if int(self.min_value.value()) + 9 > int(self.max_value.value()):
            self.max_value.setValue(int(self.min_value.value())+9)

    def change_minimum(self):
        if int(self.max_value.value()) - 9 < int(self.min_value.value()):
            self.min_value.setValue(int(self.max_value.value())-9)

    def reset(self):
        self.name.clear()
        self.min_value.setValue(1)
        self.max_value.setValue(20)


class FixedRecepieLayout(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(20)
        self.name = QtWidgets.QLineEdit()
        self.grid.addLayout(NamedWidget(title="Название предмета:", content=self.name), 1, 0)
        self.item_type = QtWidgets.QComboBox()
        self.item_type.addItems(["Сокровище", "Покеболл", "Усилитель"])
        self.grid.addLayout(NamedWidget(title="Тип предмета:", content=self.item_type), 1, 1)
        self.ing1 = QtWidgets.QLineEdit()
        self.ing2 = QtWidgets.QLineEdit()
        self.ing3 = QtWidgets.QLineEdit()
        self.ing4 = QtWidgets.QLineEdit()
        self.grid.addLayout(NamedWidget(title="Компонент 1:", content=self.ing1), 2, 0)
        self.grid.addLayout(NamedWidget(title="Компонент 2:", content=self.ing2), 2, 1)
        self.grid.addLayout(NamedWidget(title="Компонент 3:", content=self.ing3), 3, 0)
        self.grid.addLayout(NamedWidget(title="Компонент 4:", content=self.ing4), 3, 1)
        self.setLayout(self.grid)

    def reset(self):
        self.name.clear()
        self.item_type.setCurrentIndex(0)
        self.ing1.clear()
        self.ing2.clear()
        self.ing3.clear()
        self.ing4.clear()


class BaseWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        self.connection = sqlite3.connect("Pokecraft_Database.db")
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Создание предмета")
        self.resize(550, 450)
        main_layout = QtWidgets.QVBoxLayout()
        self.tabs = QtWidgets.QTabWidget()
        main_layout.addWidget(self.tabs)
        self.tab_for_craft = ForCraftLayout()
        self.tab_may_be_crafted = MayBeCraftedLayout()
        self.tab_fixed_recepie = FixedRecepieLayout()
        self.tabs.addTab(self.tab_for_craft, "Материал для создания")
        self.tabs.addTab(self.tab_may_be_crafted, "Можно создать")
        self.tabs.addTab(self.tab_fixed_recepie, "Фиксированный рецепт")
        self.create = QtWidgets.QPushButton("Внести в базу")
        self.quit = QtWidgets.QPushButton("Выход")
        self.create.clicked.connect(self.write_into_base)
        self.quit.clicked.connect(self.close)
        main_layout.addWidget(self.create)
        main_layout.addWidget(self.quit)
        self.setLayout(main_layout)

    def write_into_base(self):
        if self.tabs.currentIndex() == 0:
            self.for_craft_update()
        elif self.tabs.currentIndex() == 1:
            self.may_be_crafted_update()
        elif self.tabs.currentIndex() == 2:
            self.fixed_recipe_update()
        else:
            window_wrong = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Ошибка",
                                                 "Неверный индекс вкладки", buttons=QtWidgets.QMessageBox.Ok,
                                                 parent=self)
            window_wrong.exec()

    def for_craft_update(self):
        name = self.tab_for_craft.name.text()
        if len(name) < 4:
            window_wrong = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Ошибка",
                                                "Заполнены не все поля", buttons=QtWidgets.QMessageBox.Ok,
                                                parent=self)
            window_wrong.exec()
            return
        item_type = self.tab_for_craft.item_type.currentText()
        value = self.tab_for_craft.value.value()
        sell_price = self.tab_for_craft.price.value()
        if self.tab_for_craft.unique.isChecked():
            unique = 1
        else:
            unique = 0
        cursor = self.connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Materials (name varchar(20), item_type varchar(15), value int, 
        sell_price int, is_unique int)"""
        cursor.execute(sql)
        self.connection.commit()
        if self.check_double(name, "Materials"):
            if self.double_dialogue():
                sql = f"UPDATE Materials SET item_type = \"{item_type}\", value = {value}, " \
                      f"sell_price = {sell_price}, is_unique = {unique} WHERE name = \"{name}\""
                cursor.execute(sql)
                self.connection.commit()
                self.tab_for_craft.reset()
        else:
            sql = f"INSERT INTO Materials (name, item_type, value, sell_price, is_unique) " \
                  f"VALUES (\"{name}\", \"{item_type}\", {value}, {sell_price}, {unique})"
            cursor.execute(sql)
            self.connection.commit()
            self.tab_for_craft.reset()

    def may_be_crafted_update(self):
        name = self.tab_may_be_crafted.name.text()
        if len(name) < 5:
            window_wrong = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Ошибка",
                                                "Заполнены не все поля", buttons=QtWidgets.QMessageBox.Ok,
                                                parent=self)
            window_wrong.exec()
            return
        item_type = self.tab_may_be_crafted.item_type.currentText()
        min_value = self.tab_may_be_crafted.min_value.value()
        max_value = self.tab_may_be_crafted.max_value.value()
        cursor = self.connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Products (name varchar(20), item_type varchar(15), min_value int,
              max_value int)"""
        cursor.execute(sql)
        self.connection.commit()
        if self.check_double(name, "Products"):
            if self.double_dialogue():
                sql = f"UPDATE Products SET min_value = {min_value}, max_value = {max_value} WHERE name = \"{name}\""
                cursor.execute(sql)
                self.connection.commit()
                self.tab_may_be_crafted.reset()
        elif self.check_value():
            if self.double_dialogue(double_type="value"):
                sql = f"UPDATE Products SET name = \"{name}\", WHERE min_value = {min_value} AND max_value = {max_value}"
                cursor.execute(sql)
                self.connection.commit()
                self.tab_may_be_crafted.reset()
        else:
            sql = f"INSERT INTO Products (name, item_type, min_value, max_value)" \
                  f"VALUES (\"{name}\", \"{item_type}\", {min_value}, {max_value})"
            cursor.execute(sql)
            self.connection.commit()
            self.tab_may_be_crafted.reset()

    def fixed_recipe_update(self):
        name = self.tab_fixed_recepie.name.text()
        item_type = self.tab_fixed_recepie.item_type.currentText()
        part1 = self.tab_fixed_recepie.ing1.text()
        part2 = self.tab_fixed_recepie.ing2.text()
        part3 = self.tab_fixed_recepie.ing3.text()
        part4 = self.tab_fixed_recepie.ing4.text()
        cursor = self.connection.cursor()
        if len(part2) == 0:
            part2 = "Any"
        filled = True
        lines = (name, item_type, part1, part2, part3, part4)
        for line in lines:
            if len(line) < 3:
                filled = False
                break
        if not filled:
            window_wrong = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Ошибка",
                                                "Заполнены не все поля", buttons=QtWidgets.QMessageBox.Ok,
                                                parent=self)
            window_wrong.exec()
            return
        sql = """CREATE TABLE IF NOT EXISTS Fixed_Recipes (name varchar(20), item_type varchar(15),
                component_1 varchar(30), component_2 varchar(30), component_3 varchar(30),
                component_4 varchar(30))"""
        cursor.execute(sql)
        self.connection.commit()
        if self.check_double(name=name, table_name="Fixed_Recipes"):
            if self.double_dialogue():
                sql = f"UPDATE Fixed_Recipes SET item_type = \"{item_type}\", component_1 = \"{part1}\", " \
                      f"component_2 = \"{part2}\", component_3 = \"{part3}\", component_4 =  \"{part4}\"" \
                      f"WHERE name = \"{name}\""
                cursor.execute(sql)
                self.connection.commit()
                self.tab_fixed_recepie.reset()
        else:
            sql = f"INSERT INTO Fixed_Recipes (name, item_type, component_1, component_2, component_3, component_4) " \
                  f"VALUES (\"{name}\", \"{item_type}\", \"{part1}\", \"{part2}\", \"{part3}\", \"{part4}\")"
            cursor.execute(sql)
            self.connection.commit()
            self.tab_fixed_recepie.reset()

    def check_double(self, name, table_name):
        cursor = self.connection.cursor()
        name = name
        if self.tabs.currentIndex() == 1:
            item_type = self.tab_may_be_crafted.item_type.currentText()
            sql = f"SELECT EXISTS (SELECT * FROM {table_name} WHERE name = \"{name}\" AND item_type = \"{item_type}\")"
            cursor.execute(sql)
        else:
            sql = f"SELECT EXISTS (SELECT * FROM {table_name} WHERE name = \"{name}\")"
            cursor.execute(sql)
        if 0 not in cursor.fetchone():
            return True
        else:
            return False

    def check_value(self):
        cursor = self.connection.cursor()
        if self.tabs.currentIndex() == 0:
            value = self.tab_for_craft.value.value()
            item_type = self.tab_for_craft.item_type.currentText()
            sql = f"SELECT EXISTS (SELECT * FROM Materials WHERE value = {value} AND item_type = \"{item_type}\")"
            cursor.execute(sql)
        else:
            min_value = self.tab_may_be_crafted.min_value.value()
            max_value = self.tab_may_be_crafted.max_value.value()
            item_type = self.tab_may_be_crafted.item_type.currentText()
            sql = f"SELECT EXISTS (SELECT * FROM Products WHERE min_value = {min_value} AND " \
                  f"max_value = {max_value} AND item_type = \"{item_type}\")"
            cursor.execute(sql)
        if 0 not in cursor.fetchone():
            return True
        else:
            return False

    def double_dialogue(self, double_type="name"):
        dialog_window = ItemExistsWindow(parent=self, double_type=double_type)
        dialog_window.exec_()
        if dialog_window.update:
            return True
        else:
            return False


app = QtWidgets.QApplication(sys.argv)
window = BaseWindow()
window.show()
sys.exit(app.exec_())

