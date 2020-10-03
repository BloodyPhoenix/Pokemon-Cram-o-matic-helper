from PyQt5 import QtWidgets
import sys
import os

type_list = ("Нормальный", "Боевой", "Летающий", "Ядовитый", "Земляной", "Каменный", "Насекомый", "Призрачный",
            "Стальной", "Огненный", "Водный", "Травяной", "Электрический", "Психический", "Ледяной", "Драконий",
            "Тёмный", "Волшебный")

class NamedWidget(QtWidgets.QVBoxLayout):
    def __init__(self, title, content, parent=None):
        QtWidgets.QVBoxLayout.__init__(self, parent)
        title = QtWidgets.QLabel(str(title))
        self.addWidget(title)
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
        self.type = QtWidgets.QComboBox()
        self.type.addItems(type_list)
        self.grid.addLayout(NamedWidget(title="Тип предмета:", content=self.type), 2, 1)
        self.value = QtWidgets.QSpinBox()
        self.value.setMinimum(0)
        self.grid.addLayout(NamedWidget(title="Ценность предмета:", content=self.value), 3, 0)
        self.price = QtWidgets.QSpinBox()
        self.price.setMinimum(0)
        self.grid.addLayout(NamedWidget(title="Цена при продаже в магазине:", content=self.price), 3, 1)
        self.setLayout(self.grid)

class MayBeCraftedLayout(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(20)
        self.name = QtWidgets.QLineEdit()
        self.grid.addLayout(NamedWidget(title="Название предмета:", content=self.name), 0, 0)
        self.type = QtWidgets.QComboBox()
        self.type.addItems(type_list)
        self.grid.addLayout(NamedWidget(title="Тип предмета:", content=self.type), 0, 1)
        self.value = QtWidgets.QSpinBox()
        self.value.setMinimum(0)
        self.grid.addLayout(NamedWidget(title="Нужно очков для создания:", content=self.value), 1, 0)
        self.price = QtWidgets.QSpinBox()
        self.price.setMinimum(0)
        self.grid.addLayout(NamedWidget(title="Цена при продаже в магазине:", content=self.price), 1, 1)
        self.setLayout(self.grid)

class FixedRecepieLayout(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(20)
        self.name = QtWidgets.QLineEdit()
        self.grid.addLayout(NamedWidget(title="Название предмета:", content=self.name), 1, 0)
        self.type = QtWidgets.QComboBox()
        self.type.addItems(["Сокровище", "Покеболл"])
        self.grid.addLayout(NamedWidget(title="Тип предмета:", content=self.type), 1, 1)
        self.ing1 = QtWidgets.QLineEdit()
        self.ing2 = QtWidgets.QLineEdit()
        self.ing3 = QtWidgets.QLineEdit()
        self.ing4 = QtWidgets.QLineEdit()
        self.grid.addLayout(NamedWidget(title="Компонент 1:", content=self.ing1), 2, 0)
        self.grid.addLayout(NamedWidget(title="Компонент 2:", content=self.ing2), 2, 1)
        self.grid.addLayout(NamedWidget(title="Компонент 3:", content=self.ing3), 3, 0)
        self.grid.addLayout(NamedWidget(title="Компонент 4:", content=self.ing4), 3, 1)
        self.setLayout(self.grid)

class BaseWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Создание предмета")
        self.resize(550, 450)
        main_layout = QtWidgets.QVBoxLayout()
        tabs = QtWidgets.QTabWidget()
        main_layout.addWidget(tabs)
        self.tab_for_craft = ForCraftLayout()
        self.tab_may_be_crafted = MayBeCraftedLayout()
        self.tab_fixed_recepie = FixedRecepieLayout()
        tabs.addTab(self.tab_for_craft, "Материал для создания")
        tabs.addTab(self.tab_may_be_crafted, "Можно создать")
        tabs.addTab(self.tab_fixed_recepie, "Фиксированный рецепт")
        self.create = QtWidgets.QPushButton("Внести в базу")
        self.quit = QtWidgets.QPushButton("Выход")
        self.quit.clicked.connect(self.close)
        main_layout.addWidget(self.create)
        main_layout.addWidget(self.quit)
        self.setLayout(main_layout)

app = QtWidgets.QApplication(sys.argv)
window = BaseWindow()
window.show()
sys.exit(app.exec_())


            
    
        

    
