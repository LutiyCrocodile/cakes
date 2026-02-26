import datetime
from fileinput import filename
from logging import exception

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt, QIODevice
from PyQt6.QtWidgets import QMessageBox

from db_helper import db

import sys



class MainWin(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Магазин тортов")
        self.icon = QtGui.QIcon("icon.png")
        self.setWindowIcon(self.icon)
        self.resize(1000, 800)

        # Запрос данных из БД
        self.data_clients = db.query("SELECT * FROM clients")
        self.data_cakes = db.query("SELECT * FROM cakes")
        self.data_orders = db.query("SELECT * FROM orders")

        self.setStyleSheet("font-size:20px")

        self.layout = QtWidgets.QVBoxLayout()

        self.stack = QtWidgets.QStackedLayout()


        if len(self.data_cakes) <= 5:
            page = QtWidgets.QFrame()
            self.page_lay = QtWidgets.QVBoxLayout(page)

            scroll = QtWidgets.QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

            frame_scroll = QtWidgets.QFrame()
            scroll_lay = QtWidgets.QVBoxLayout(frame_scroll)

            scroll.setWidget(frame_scroll)

            self.login_btn = QtWidgets.QPushButton("Войти")
            self.login_btn_lay = QtWidgets.QHBoxLayout()
            self.login_btn_lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            self.login_btn_lay.addWidget(self.login_btn)
            self.login_btn.clicked.connect(self.login)

            scroll_lay.addLayout(self.login_btn_lay)

            for i, data in enumerate(self.data_cakes):
                lbl = QtWidgets.QLabel()
                lay_for_cake = QtWidgets.QHBoxLayout(frame_scroll)
                pix = QtGui.QPixmap()
                pix.loadFromData(self.data_cakes[i]["photo"])
                lbl.setPixmap(pix.scaled(250, 250))
                lay_for_cake.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                lay_for_cake.addWidget(lbl)
                lay_for_cake.addWidget(QtWidgets.QLabel(self.data_cakes[i]["name"]))
                scroll_lay.addLayout(lay_for_cake)



            self.page_lay.addWidget(scroll)
            self.stack.addWidget(page)

        else:
            pages = int(len(self.data_cakes) / 5)
            for i in range(pages+1):

                page = QtWidgets.QFrame()
                self.page_lay = QtWidgets.QVBoxLayout(page)

                scroll = QtWidgets.QScrollArea()
                scroll.setWidgetResizable(True)
                scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

                scroll_frame = QtWidgets.QFrame()
                scroll_lay = QtWidgets.QVBoxLayout(scroll_frame)

                scroll.setWidget(scroll_frame)

                self.login_btn = QtWidgets.QPushButton("Войти")
                self.lbl_main = QtWidgets.QLabel("Магазин тортов")
                self.lay_for_main_lbl = QtWidgets.QHBoxLayout()
                self.lay_for_main_lbl.addWidget(self.lbl_main)
                self.login_btn.setStyleSheet(
                    "QPushButton { border-radius: 10px; background-color: #dfdfdf; border: 1px solid #333; font-size:16px; padding:5px;} "
                    "QPushButton:hover {background-color: #d3d3d3} "
                    "QPushButton:pressed {background-color: #f3f3f3}")
                self.login_btn_lay = QtWidgets.QHBoxLayout()
                self.main_up_lay = QtWidgets.QHBoxLayout()
                self.main_up_lay.addLayout(self.lay_for_main_lbl)
                self.main_up_lay.addLayout(self.login_btn_lay)
                self.login_btn_lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
                self.login_btn_lay.addWidget(self.login_btn)
                self.login_btn.clicked.connect(self.login)

                self.page_lay.addLayout(self.main_up_lay)

                for j, data in enumerate(self.data_cakes[5*i:5*i+5]):
                    lbl = QtWidgets.QLabel()
                    lay_for_cake = QtWidgets.QHBoxLayout()
                    pix = QtGui.QPixmap()
                    pix.loadFromData(self.data_cakes[i*5+j]["photo"])
                    lbl.setPixmap(pix.scaled(250, 250))
                    lay_for_cake.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                    lay_for_cake.addWidget(lbl)
                    btn_zakaz = QtWidgets.QPushButton("Заказать")
                    btn_zakaz.clicked.connect(self.show_message)
                    btn_zakaz.setStyleSheet("QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
                                            "QPushButton:hover {background-color: #d3d3d3} "
                                            "QPushButton:pressed {background-color: #f3f3f3}")
                    lay_for_cake.addWidget(QtWidgets.QLabel(self.data_cakes[i*5+j]["name"]))
                    lay_for_cake.addWidget(btn_zakaz)
                    scroll_lay.addLayout(lay_for_cake)

                btn_back = QtWidgets.QPushButton("Назад")
                btn_back.setStyleSheet(
                    "QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
                    "QPushButton:hover {background-color: #d3d3d3} "
                    "QPushButton:pressed {background-color: #f3f3f3}")
                btn_forward = QtWidgets.QPushButton("Вперед")
                btn_forward.setStyleSheet(
                    "QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
                    "QPushButton:hover {background-color: #d3d3d3} "
                    "QPushButton:pressed {background-color: #f3f3f3}")
                btn_lay = QtWidgets.QHBoxLayout()
                btn_lay.addWidget(btn_back)
                btn_lay.addWidget(btn_forward)
                self.page_lay.addWidget(scroll)
                self.page_lay.addLayout(btn_lay)
                btn_back.clicked.connect(self.go_to_page_down)
                btn_forward.clicked.connect(self.go_to_page_up)


                self.stack.addWidget(page)



        self.stack.setCurrentIndex(0)

        self.layout.addLayout(self.stack)

        self.setLayout(self.layout)


    def go_to_page_down(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() - 1)

    def go_to_page_up(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() + 1)

    def login(self):
        self.dialog = QtWidgets.QDialog()
        # self.dialog.setHidden(False)
        self.dialog.setWindowIcon(self.icon)
        self.dialog.setWindowTitle("Войти")
        self.dialog.resize(300, 200)
        dialog_lay = QtWidgets.QVBoxLayout()
        lbl = QtWidgets.QLabel("Вход")
        self.line_edit_login = QtWidgets.QLineEdit()
        self.line_edit_login.setStyleSheet("padding: 5px")
        self.line_edit_password = QtWidgets.QLineEdit()
        self.line_edit_password.setStyleSheet("padding: 5px")
        self.line_edit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        btn_enter = QtWidgets.QPushButton("Войти")
        btn_enter.clicked.connect(self.enter)
        btn_register = QtWidgets.QPushButton("Зарегистрироваться")
        btn_register.clicked.connect(self.register)
        btn_enter.setStyleSheet(
            "QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
            "QPushButton:hover {background-color: #d3d3d3} "
            "QPushButton:pressed {background-color: #f3f3f3}")
        btn_register.setStyleSheet(
            "QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
            "QPushButton:hover {background-color: #d3d3d3} "
            "QPushButton:pressed {background-color: #f3f3f3}")
        btn_lay = QtWidgets.QHBoxLayout()
        btn_lay.addWidget(btn_enter)
        btn_lay.addWidget(btn_register)
        lbl.setStyleSheet("font-size:20px; font-weight:bold;")
        dialog_lay.addWidget(lbl)
        dialog_lay.addWidget(self.line_edit_login)
        dialog_lay.addWidget(self.line_edit_password)
        dialog_lay.addLayout(btn_lay)
        dialog_lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.dialog.setLayout(dialog_lay)
        self.dialog.exec()


    def register(self):
        self.reg_win = RegUser()
        self.reg_win.show()
        self.dialog.close()


    def enter(self):
        self.client = db.query(f"SELECT * FROM clients WHERE login = '{self.line_edit_login.text()}' and password = '{self.line_edit_password.text()}'")
        if self.client:
            self.login_btn.setHidden(True)
            self.win = Logined(self.client)
            self.win.show()
            self.close()
            self.dialog.close()
        else:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль")

    def show_message(self):
        QtWidgets.QMessageBox.critical(self, "Ошибка", "Сначала войдите или зарегистрируйтесь!")



class RegUser(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # self.dialog.setHidden(True)
        # self.dialog.close()
        # self.dialog_reg = QtWidgets.QDialog()
        self.resize(800, 600)
        self.dialog_reg_lay = QtWidgets.QVBoxLayout()
        self.setWindowTitle("Регистрация")
        self.icon = QtGui.QIcon("icon.png")
        self.setWindowIcon(self.icon)

        self.le_name_reg = QtWidgets.QLineEdit()
        self.le_name_reg.setPlaceholderText("Имя...")
        self.le_surname_reg = QtWidgets.QLineEdit()
        self.le_surname_reg.setPlaceholderText("Фамилия...")
        self.le_email_reg = QtWidgets.QLineEdit()
        self.le_email_reg.setPlaceholderText("Почта...")
        email_val = QtGui.QRegularExpressionValidator(
            QtCore.QRegularExpression("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.-]+\.[a-zA-Z+]+$"), self.le_email_reg)
        self.le_email_reg.setValidator(email_val)
        self.le_phone_reg = QtWidgets.QLineEdit()
        self.le_phone_reg.setPlaceholderText("Телефон...")
        self.le_phone_reg.setInputMask("+7-999-999-99-99")
        self.le_login_reg = QtWidgets.QLineEdit()
        self.le_login_reg.setPlaceholderText("Логин...")
        self.le_password_reg = QtWidgets.QLineEdit()
        self.le_password_reg.setPlaceholderText("Пароль...")
        self.lbl_for_photo = QtWidgets.QLabel()
        self.lbl_for_photo.setHidden(True)
        self.pix_photo = QtGui.QPixmap()

        self.lay_info_reg = QtWidgets.QVBoxLayout()
        self.lay_btn_reg = QtWidgets.QVBoxLayout()
        self.lay_btn_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.lbl_reg = QtWidgets.QLabel("Регистрация")
        self.lbl_reg.setStyleSheet("border: none; font-size: 26px;")
        self.lbl_reg.setMaximumHeight(50)

        self.lay_info_reg.addWidget(self.lbl_reg)
        self.lay_info_reg.addWidget(self.le_name_reg)
        self.lay_info_reg.addWidget(self.le_surname_reg)
        self.lay_info_reg.addWidget(self.le_email_reg)
        self.lay_info_reg.addWidget(self.le_phone_reg)
        self.lay_info_reg.addWidget(self.le_login_reg)
        self.lay_info_reg.addWidget(self.le_password_reg)
        self.lay_info_reg.addWidget(self.lbl_for_photo)

        self.btn_load_image = QtWidgets.QPushButton("Загрузить изображение")
        self.btn_load_image.setMaximumWidth(200)
        self.btn_load_image.clicked.connect(self.load_image)
        self.btn_load_image.setStyleSheet(
            "QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
            "QPushButton:hover {background-color: #d3d3d3} "
            "QPushButton:pressed {background-color: #f3f3f3}")
        self.lay_info_reg.addWidget(self.btn_load_image)

        self.btn_register = QtWidgets.QPushButton("Зарегистрироваться")
        self.btn_register.clicked.connect(self.register)
        self.btn_register.setStyleSheet(
            "QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
            "QPushButton:hover {background-color: #d3d3d3} "
            "QPushButton:pressed {background-color: #f3f3f3}")
        self.btn_register.setMinimumWidth(500)


        self.lay_btn_reg.addWidget(self.btn_register)

        self.dialog_reg_lay.addLayout(self.lay_info_reg)
        self.dialog_reg_lay.addLayout(self.lay_btn_reg)

        self.setLayout(self.dialog_reg_lay)

        self.setStyleSheet(
            "QLineEdit{border: 1px solid #222; border-radius: 10px; font-size: 20px;}")

    def load_image(self):
        self.file_dialog = QtWidgets.QFileDialog.getOpenFileName(self, "Фото", '/', 'JPG File (*.jpg);; PNG File (*.png)')
        self.url = self.file_dialog[0]
        self.pix_photo.load(self.url)
        self.lbl_for_photo.setPixmap(self.pix_photo.scaled(200, 200))
        self.lbl_for_photo.setHidden(False)

    def register(self):
        unique = db.query(f"SELECT * FROM clients WHERE login = '{self.le_login_reg.text()}'")
        # photo = self.convertToBinaryData(self.url)
        if (len(self.le_name_reg.text()) > 0
                and len(self.le_surname_reg.text()) > 0
                and len(self.le_email_reg.text()) > 0
                and len(self.le_phone_reg.text()) > 0
                and len(self.le_login_reg.text()) > 0
                and len(self.le_password_reg.text()) > 0) and not unique and len(self.le_phone_reg.text()) == 16 and self.le_email_reg.hasAcceptableInput():
            db.query(f"INSERT INTO clients (name, surname, phone, email, login, password, photo) VALUES ('{self.le_name_reg.text()}', "
                     f"'{self.le_surname_reg.text()}', "
                     f"'{self.le_phone_reg.text()}', "
                     f"'{self.le_email_reg.text()}', "
                     f"'{self.le_login_reg.text()}', "
                     f"'{self.le_password_reg.text()}', "
                     f"'{self.convertToBinaryData(self.url)}')")
        elif unique:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Такой пользователь уже существует!")
        elif len(self.le_phone_reg.text()) != 16:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Неверно введен телефон")
        elif not self.le_email_reg.hasAcceptableInput():
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Неверно введена почта")
        else:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Не все поля заполнены!")

    def convertToBinaryData(self, file_path):
            with open(file_path, 'rb') as f:
                data = f.read()
            return data


class Logined(QtWidgets.QWidget):
    def __init__(self, client_data:list):
        super().__init__()
        self.setWindowTitle("Магазин тортов")
        print(client_data)
        self.icon = QtGui.QIcon("icon.png")
        self.client = client_data
        self.setWindowIcon(self.icon)
        self.resize(1000, 800)

        # Запрос данных из БД
        self.data_clients = db.query("SELECT * FROM clients")
        self.data_cakes = db.query("SELECT * FROM cakes")
        self.data_orders = db.query("SELECT * FROM orders")

        self.setStyleSheet("font-size:20px")

        self.layout = QtWidgets.QVBoxLayout()

        self.stack = QtWidgets.QStackedLayout()

        self.menu = QtWidgets.QMenuBar()
        self.menu_item = QtWidgets.QMenu("Личный кабинет")
        about = self.menu_item.addAction("О пользователе")
        korz = self.menu_item.addAction("Корзина")
        logout = self.menu_item.addAction("Выйти")
        about.triggered.connect(self.about)
        korz.triggered.connect(self.korz)
        logout.triggered.connect(self.logout)
        self.menu.addMenu(self.menu_item)


        self.layout.addWidget(self.menu)
        self.korzina = {}

        if len(self.data_cakes) <= 5:
            page = QtWidgets.QFrame()
            self.page_lay = QtWidgets.QVBoxLayout(page)

            scroll = QtWidgets.QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

            frame_scroll = QtWidgets.QFrame()
            scroll_lay = QtWidgets.QVBoxLayout(frame_scroll)

            scroll.setWidget(frame_scroll)


            for i, data in enumerate(self.data_cakes):
                lbl = QtWidgets.QLabel()
                lay_for_cake = QtWidgets.QHBoxLayout(frame_scroll)
                pix = QtGui.QPixmap()
                pix.loadFromData(self.data_cakes[i]["photo"])
                lbl.setPixmap(pix.scaled(250, 250))
                lay_for_cake.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                lay_for_cake.addWidget(lbl)
                lay_for_cake.addWidget(QtWidgets.QLabel(self.data_cakes[i]["name"]))
                scroll_lay.addLayout(lay_for_cake)

            self.page_lay.addWidget(scroll)
            self.stack.addWidget(page)

        else:
            pages = int(len(self.data_cakes) / 5)
            for i in range(pages + 1):

                page = QtWidgets.QFrame()
                self.page_lay = QtWidgets.QVBoxLayout(page)

                scroll = QtWidgets.QScrollArea()
                scroll.setWidgetResizable(True)
                scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

                scroll_frame = QtWidgets.QFrame()
                scroll_lay = QtWidgets.QVBoxLayout(scroll_frame)

                scroll.setWidget(scroll_frame)

                for j, data in enumerate(self.data_cakes[5 * i:5 * i + 5]):
                    lbl = QtWidgets.QLabel()
                    lay_for_cake = QtWidgets.QHBoxLayout()
                    pix = QtGui.QPixmap()
                    pix.loadFromData(self.data_cakes[i * 5 + j]["photo"])
                    lbl.setPixmap(pix.scaled(250, 250))
                    lay_for_cake.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                    lay_for_cake.addWidget(lbl)
                    btn_zakaz = QtWidgets.QPushButton("Заказать")
                    btn_zakaz.setStyleSheet(
                        "QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
                        "QPushButton:hover {background-color: #d3d3d3} "
                        "QPushButton:pressed {background-color: #f3f3f3}")
                    btn_zakaz.setObjectName(f'cake {self.data_cakes[i * 5 + j]["id"]}')
                    self.korzina[btn_zakaz.objectName()] = 0
                    btn_zakaz.clicked.connect(self.add_cake)
                    lay_for_cake.addWidget(QtWidgets.QLabel(self.data_cakes[i * 5 + j]["name"]))
                    lay_for_cake.addWidget(btn_zakaz)
                    scroll_lay.addLayout(lay_for_cake)

                btn_back = QtWidgets.QPushButton("Назад")
                btn_back.setStyleSheet(
                    "QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
                    "QPushButton:hover {background-color: #d3d3d3} "
                    "QPushButton:pressed {background-color: #f3f3f3}")
                btn_forward = QtWidgets.QPushButton("Вперед")
                btn_forward.setStyleSheet(
                    "QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
                    "QPushButton:hover {background-color: #d3d3d3} "
                    "QPushButton:pressed {background-color: #f3f3f3}")
                btn_lay = QtWidgets.QHBoxLayout()
                btn_lay.addWidget(btn_back)
                btn_lay.addWidget(btn_forward)
                self.page_lay.addWidget(scroll)
                self.page_lay.addLayout(btn_lay)
                btn_back.clicked.connect(self.to_page_down)
                btn_forward.clicked.connect(self.to_page_up)

                self.stack.addWidget(page)

        self.stack.setCurrentIndex(0)



        self.layout.addLayout(self.stack)

        self.setLayout(self.layout)

    def add_cake(self):
        self.korzina[self.sender().objectName()] += 1
        print(self.korzina)

    def to_page_down(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() - 1)

    def to_page_up(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() + 1)

    def about(self):
        self.cabinet = Cabinet(self.client[0])
        self.cabinet.show()

    def korz(self):
        self.win = Korz(self.korzina, *self.client)
        self.win.show()
        self.close()

    def logout(self):
        self.logout_now = MainWin()
        self.logout_now.show()
        self.close()


class Korz(QtWidgets.QWidget):
    def __init__(self, korz: dict, client_data: dict):
        super().__init__()
        self.setWindowTitle("Корзина")
        self.icon = QtGui.QIcon("icon.png")
        self.setWindowIcon(self.icon)
        self.resize(1000, 800)
        self.korz = korz
        self.client_data = client_data


        self.lay = QtWidgets.QVBoxLayout()

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_frame = QtWidgets.QFrame()
        self.scroll_lay = QtWidgets.QVBoxLayout(self.scroll_frame)
        self.scroll.setWidget(self.scroll_frame)

        self.non_neg = {k: v for k, v in self.korz.items() if v > 0}
        print(*self.non_neg.keys())
        # ng = [non_neg.keys()]

        for i in self.non_neg.keys():
            self.lay_for_cake = QtWidgets.QHBoxLayout()
            self.cake_data = db.query(f"SELECT * FROM cakes WHERE id = '{i.split(' ')[-1]}'")
            print(self.non_neg[i])
            self.lbl = QtWidgets.QLabel()
            self.pix_for_lbl = QtGui.QPixmap()
            self.pix_for_lbl.loadFromData(self.cake_data[0]["photo"])
            self.lbl_name = QtWidgets.QLabel(f'Название: {self.cake_data[0]["name"]}')
            self.lbl_name.setMaximumHeight(50)
            self.lbl_name.setStyleSheet("font-size:20px;")
            self.lbl_quantity = QtWidgets.QLabel(f"Количество: {str(self.non_neg[i])}")
            self.lbl_quantity.setStyleSheet("font-size:20px;")
            self.lbl_quantity.setMaximumHeight(50)
            self.lbl_quantity.setObjectName(i)
            self.lay_cake = QtWidgets.QVBoxLayout()
            self.lay_cake.addWidget(self.lbl_name)
            self.lay_cake.addWidget(self.lbl_quantity)
            self.btn_minus = QtWidgets.QPushButton("➖")
            self.btn_minus.setObjectName(f"{i}")
            self.btn_minus.setMaximumWidth(50)
            self.btn_minus.clicked.connect(self.minus)
            self.btn_minus.setStyleSheet(
                    "QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
                    "QPushButton:hover {background-color: #d3d3d3} "
                    "QPushButton:pressed {background-color: #f3f3f3}")
            self.btn_plus = QtWidgets.QPushButton("➕")
            self.btn_plus.setObjectName(f"{i}")
            self.btn_plus.setMaximumWidth(50)
            self.btn_plus.clicked.connect(self.plus)
            self.btn_plus.setStyleSheet(
                    "QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
                    "QPushButton:hover {background-color: #d3d3d3} "
                    "QPushButton:pressed {background-color: #f3f3f3}")
            self.lay_for_cake.addWidget(self.lbl)
            self.lay_for_cake.addLayout(self.lay_cake)
            self.lay_for_cake.addWidget(self.btn_minus)
            self.lay_for_cake.addWidget(self.btn_plus)
            self.lbl.setPixmap(self.pix_for_lbl.scaled(250, 250))
            self.scroll_lay.addLayout(self.lay_for_cake)

        self.lbl_main = QtWidgets.QLabel("Корзина")
        self.lbl_main.setStyleSheet("font-size: 28px")
        self.lay.addWidget(self.lbl_main)
        self.lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(self.scroll)

        self.btn_back_to_shop = QtWidgets.QPushButton("Назад")
        self.btn_back_to_shop.clicked.connect(self.go_back)
        self.btn_back_to_shop.setStyleSheet(
                    "QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
                    "QPushButton:hover {background-color: #d3d3d3} "
                    "QPushButton:pressed {background-color: #f3f3f3}")
        self.btn_commit_shop = QtWidgets.QPushButton("Оплатить")
        self.btn_commit_shop.setStyleSheet(
                    "QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
                    "QPushButton:hover {background-color: #d3d3d3} "
                    "QPushButton:pressed {background-color: #f3f3f3}")
        self.btn_lay = QtWidgets.QHBoxLayout()
        self.btn_lay.addWidget(self.btn_back_to_shop)
        self.btn_lay.addWidget(self.btn_commit_shop)

        self.lay.addLayout(self.btn_lay)

        self.setLayout(self.lay)

    def go_back(self):
        self.win = Logined([self.client_data])
        self.win.show()
        self.close()

    def minus(self):
        # if self.korz[f"{self.sender().objectName().split(' ')[-1]}"] >= 0:
        # print(self.korz[f"{self.sender().objectName().split('-')[-1]}"])
        # self.korz[f"{self.sender().objectName().split('-')[-1]}"] -= 1
            # self.lbl_quantity.setText(self.korz[f"{self.sender().objectName()}"])
            # self.update()
        # else:
        # self.korz[f"{self.sender().objectName().split('-')[-1]}"] = 0
        self.korz[f'{self.sender().objectName()}'] -= 1 if self.korz[f'{self.sender().objectName()}'] > 1 else self.korz[f'{self.sender().objectName()}'] == 0
        print(self.korz)



    def plus(self):
        # self.lbl_quantity.setText(self.korz[f"{self.sender().objectName().split(' ')[-1]}"])
        # self.update()
        self.korz[f'{self.sender().objectName()}'] += 1

        print(self.korz)
        self.update()






class Cabinet(QtWidgets.QWidget):
    def __init__(self, user: dict):
        super().__init__()
        self.resize(700, 450)
        self.setWindowTitle("Профиль")
        self.icon = QtGui.QIcon("icon.png")
        self.setWindowIcon(self.icon)
        self.user = user

        self.lay = QtWidgets.QVBoxLayout()
        self.lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.client_lay_1 = QtWidgets.QHBoxLayout()
        self.client_lay_2 = QtWidgets.QHBoxLayout()
        self.client_lay_3 = QtWidgets.QHBoxLayout()
        self.client_lay_4 = QtWidgets.QHBoxLayout()
        self.client_lay_5 = QtWidgets.QHBoxLayout()

        self.lbl = QtWidgets.QLabel()
        self.lbl.setStyleSheet("border: 4px solid #222; border-radius:10px;")
        self.pix = QtGui.QPixmap()
        self.pix.loadFromData(user["photo"])
        self.lbl.setPixmap(self.pix.scaled(350, 200))

        self.lbl_photo = QtWidgets.QLabel("Фото: ")
        self.lbl_name = QtWidgets.QLabel("Имя: ")
        self.lbl_surname = QtWidgets.QLabel("Фамилия: ")
        self.lbl_phone = QtWidgets.QLabel("Телефон: ")
        self.lbl_email = QtWidgets.QLabel("Почта: ")

        self.le_name = QtWidgets.QLineEdit()
        self.le_name.setText(self.user['name'])
        self.le_name.setEnabled(False)
        self.le_surname = QtWidgets.QLineEdit()
        self.le_surname.setText(self.user['surname' ])
        self.le_surname.setEnabled(False)
        self.le_email = QtWidgets.QLineEdit()
        self.le_email.setText(self.user['email'])
        self.le_email.setEnabled(False)
        valid_email = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(r"^[0-9a-zA-Z_.+-]+@[0-9a-zA-Z.-]+\.[a-zA-Z0-9-.]+$"), self.le_email)
        self.le_email.setValidator(valid_email)
        self.le_phone = QtWidgets.QLineEdit()
        self.le_phone.setInputMask("+7-999-999-99-99")
        self.le_phone.setText(self.user['phone'])
        self.le_phone.setEnabled(False)

        self.client_lay_1.addWidget(self.lbl_photo)
        self.client_lay_1.addWidget(self.lbl)
        self.client_lay_2.addWidget(self.lbl_name)
        self.client_lay_2.addWidget(self.le_name)
        self.client_lay_3.addWidget(self.lbl_surname)
        self.client_lay_3.addWidget(self.le_surname)
        self.client_lay_4.addWidget(self.lbl_email)
        self.client_lay_4.addWidget(self.le_email)
        self.client_lay_5.addWidget(self.lbl_phone)
        self.client_lay_5.addWidget(self.le_phone)

        self.setStyleSheet("font-size: 20px;")

        self.lay.addLayout(self.client_lay_1)
        self.lay.addLayout(self.client_lay_2)
        self.lay.addLayout(self.client_lay_3)
        self.lay.addLayout(self.client_lay_4)
        self.lay.addLayout(self.client_lay_5)

        self.btn_edit = QtWidgets.QPushButton("Редактировать информацию")
        self.btn_edit.setStyleSheet("QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
                        "QPushButton:hover {background-color: #d3d3d3} "
                        "QPushButton:pressed {background-color: #f3f3f3}")
        self.btn_edit.clicked.connect(self.change_info)
        self.btn_change_pass = QtWidgets.QPushButton("Изменить пароль")
        self.btn_change_pass.setStyleSheet("QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
                        "QPushButton:hover {background-color: #d3d3d3} "
                        "QPushButton:pressed {background-color: #f3f3f3}")
        self.btn_change_pass.clicked.connect(self.change_password)
        self.btn_lay = QtWidgets.QHBoxLayout()
        self.btn_lay.addWidget(self.btn_change_pass)
        self.btn_lay.addWidget(self.btn_edit)
        self.lay.addLayout(self.btn_lay)

        self.setLayout(self.lay)

    def change_password(self):
        self.dialog = QtWidgets.QDialog()
        self.dialog.setWindowTitle("Смена пароля")
        self.dialog.setWindowIcon(self.icon)
        self.dialog_lay = QtWidgets.QVBoxLayout()
        self.dialog.setLayout(self.dialog_lay)

        self.lbl_change = QtWidgets.QLabel("Изменение пароля")
        # self.dialog.setStyleSheet("font-size: 20px;")

        self.lay_change_pwd_1 = QtWidgets.QHBoxLayout()
        self.lay_change_pwd_2 = QtWidgets.QHBoxLayout()
        self.lay_change_pwd_3 = QtWidgets.QHBoxLayout()

        self.lbl_last_pwd = QtWidgets.QLabel("Старый пароль: ")
        self.lbl_new_pwd = QtWidgets.QLabel("Новый пароль: ")
        self.lbl_new_pwd_check = QtWidgets.QLabel("Подтвердите новый пароль: ")

        self.le_last_pwd = QtWidgets.QLineEdit()
        self.le_last_pwd.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.le_new_pwd = QtWidgets.QLineEdit()
        self.le_new_pwd.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.le_new_pwd_check = QtWidgets.QLineEdit()
        self.le_new_pwd_check.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.lay_change_pwd_1.addWidget(self.lbl_last_pwd)
        self.lay_change_pwd_1.addWidget(self.le_last_pwd)
        self.lay_change_pwd_2.addWidget(self.lbl_new_pwd)
        self.lay_change_pwd_2.addWidget(self.le_new_pwd)
        self.lay_change_pwd_3.addWidget(self.lbl_new_pwd_check)
        self.lay_change_pwd_3.addWidget(self.le_new_pwd_check)

        self.btn_lay_change_pwd = QtWidgets.QHBoxLayout()
        self.btn_change_pwd = QtWidgets.QPushButton("Подтвердить")
        self.btn_change_pwd.setStyleSheet(
            "QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
            "QPushButton:hover {background-color: #d3d3d3} "
            "QPushButton:pressed {background-color: #f3f3f3}")
        self.btn_change_pwd.clicked.connect(self.apply_change_pwd)
        self.btn_cancel_change_pwd = QtWidgets.QPushButton("Отмена")
        self.btn_cancel_change_pwd.setStyleSheet(
            "QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
            "QPushButton:hover {background-color: #d3d3d3} "
            "QPushButton:pressed {background-color: #f3f3f3}")
        self.btn_cancel_change_pwd.clicked.connect(self.cancel_changes)
        self.btn_lay_change_pwd.addWidget(self.btn_change_pwd)
        self.btn_lay_change_pwd.addWidget(self.btn_cancel_change_pwd)

        self.dialog_lay.addWidget(self.lbl_change)
        self.dialog_lay.addLayout(self.lay_change_pwd_1)
        self.dialog_lay.addLayout(self.lay_change_pwd_2)
        self.dialog_lay.addLayout(self.lay_change_pwd_3)
        self.dialog_lay.addLayout(self.btn_lay_change_pwd)
        self.dialog_lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.dialog.exec()

    def change_info(self):
        self.le_name.setEnabled(True)
        self.le_surname.setEnabled(True)
        self.le_email.setEnabled(True)
        self.le_phone.setEnabled(True)
        self.btn_change_info = QtWidgets.QPushButton("Принять")
        self.btn_change_info.setStyleSheet("QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
                        "QPushButton:hover {background-color: #d3d3d3} "
                        "QPushButton:pressed {background-color: #f3f3f3}")
        self.btn_change_info.clicked.connect(self.commit_info)
        self.btn_lay.addWidget(self.btn_change_info)
        self.btn_edit.setHidden(True)

    def commit_info(self):
        if self.le_email.hasAcceptableInput() and len(self.le_phone.text()) == 16:
            self.le_name.setEnabled(False)
            self.le_surname.setEnabled(False)
            self.le_email.setEnabled(False)
            self.le_phone.setEnabled(False)
            self.btn_change_info.setHidden(True)
            self.btn_edit.setHidden(False)
            db.query(f"UPDATE clients SET name = '{self.le_name.text()}', surname = '{self.le_surname.text()}', email = '{self.le_email.text()}', phone = '{self.le_phone.text()}' WHERE id = {self.user['id']}")
        else:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Неверно введена почта или телефон!")


    def apply_change_pwd(self):
        user_data = db.query(f"SELECT * FROM clients WHERE id = '{self.user['id']}'")
        if self.le_last_pwd.text() == user_data[0]['password'] and self.le_new_pwd.text() == self.le_new_pwd_check.text():
            db.query(f"UPDATE clients SET password = '{self.le_new_pwd.text()}' WHERE id = {user_data[0]['id']}")
            QtWidgets.QMessageBox.information(self, "Успех", "Пароль успешно обновлен!")
            self.dialog.close()
        elif self.le_last_pwd.text() != user_data[0]['password']:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Неверный пароль!")
        elif self.le_new_pwd.text() != self.le_new_pwd_check.text():
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Пароли не совпадают!")
        else:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Не все поля заполнены!")

    def cancel_changes(self):
        self.dialog.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec())
