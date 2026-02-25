import datetime
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
        self.line_edit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
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
        self.cabinet = Cabinet(self.client[0])
        self.cabinet.show()

    def korz(self):
        print("AAAAAA")

    def logout(self):
        print("AAAAAA")




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
        if self.le_email.hasAcceptableInput():
            self.le_name.setEnabled(False)
            self.le_surname.setEnabled(False)
            self.le_email.setEnabled(False)
            self.le_phone.setEnabled(False)
            self.btn_change_info.setHidden(True)
            self.btn_edit.setHidden(False)
            db.query(f"UPDATE clients SET name = '{self.le_name.text()}', surname = '{self.le_surname.text()}', email = '{self.le_email.text()}', phone = '{self.le_phone.text()}' WHERE id = {self.user['id']}")
        else:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Неверно введена почта!")


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
