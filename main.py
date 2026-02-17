from fileinput import filename

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt
from db_helper import db

import sys



class MainWin(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Магазин тортов")
        self.icon = QtGui.QIcon("icon.png")
        self.setWindowIcon(self.icon)
        self.resize(700, 500)

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
                lbl.setPixmap(pix.scaled(100, 100))
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
                self.login_btn.setStyleSheet(
                    "QPushButton { border-radius: 10px; background-color: #dfdfdf; border: 1px solid #333; font-size:16px; padding:5px;} "
                    "QPushButton:hover {background-color: #d3d3d3} "
                    "QPushButton:pressed {background-color: #f3f3f3}")
                self.login_btn_lay = QtWidgets.QHBoxLayout()
                self.login_btn_lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
                self.login_btn_lay.addWidget(self.login_btn)
                self.login_btn.clicked.connect(self.login)

                self.page_lay.addLayout(self.login_btn_lay)

                for j, data in enumerate(self.data_cakes[5*i:5*i+5]):
                    lbl = QtWidgets.QLabel()
                    lay_for_cake = QtWidgets.QHBoxLayout()
                    pix = QtGui.QPixmap()
                    pix.loadFromData(self.data_cakes[i*5+j]["photo"])
                    lbl.setPixmap(pix.scaled(100, 100))
                    lay_for_cake.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                    lay_for_cake.addWidget(lbl)
                    btn_zakaz = QtWidgets.QPushButton("Заказать")
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
        self.dialog.setWindowIcon(self.icon)
        self.dialog.setWindowTitle("Войти")
        self.dialog.resize(300, 200)
        dialog_lay = QtWidgets.QVBoxLayout()
        lbl = QtWidgets.QLabel("Вход")
        self.line_edit_login = QtWidgets.QLineEdit()
        self.line_edit_login.setStyleSheet("padding: 5px")
        self.line_edit_password = QtWidgets.QLineEdit()
        self.line_edit_password.setStyleSheet("padding: 5px")
        btn_enter = QtWidgets.QPushButton("Войти")
        btn_enter.clicked.connect(self.enter)
        btn_register = QtWidgets.QPushButton("Зарегистрироваться")
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

    def enter(self):
        client = db.query(f"SELECT * FROM clients WHERE login = '{self.line_edit_login.text()}' and password = '{self.line_edit_password.text()}'")
        if client:
            self.login_btn.setHidden(True)
            self.win = Logined(client)
            self.win.show()
            self.close()
            self.dialog.close()
        else:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль")


class Logined(QtWidgets.QWidget):
    def __init__(self, client_data:list):
        super().__init__()
        self.setWindowTitle("Магазин тортов")
        print(client_data)
        self.icon = QtGui.QIcon("icon.png")
        self.setWindowIcon(self.icon)
        self.resize(700, 500)

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
                lbl.setPixmap(pix.scaled(100, 100))
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
                    lbl.setPixmap(pix.scaled(100, 100))
                    lay_for_cake.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                    lay_for_cake.addWidget(lbl)
                    btn_zakaz = QtWidgets.QPushButton("Заказать")
                    btn_zakaz.setStyleSheet(
                        "QPushButton { border-radius: 10px; background-color: #dfdfdf; padding: 5px; border: 1px solid #333;} "
                        "QPushButton:hover {background-color: #d3d3d3} "
                        "QPushButton:pressed {background-color: #f3f3f3}")
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

    def to_page_down(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() - 1)

    def to_page_up(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() + 1)

    def about(self):
        print("AAAAAA")

    def korz(self):
        print("AAAAAA")

    def logout(self):
        print("AAAAAA")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec())
