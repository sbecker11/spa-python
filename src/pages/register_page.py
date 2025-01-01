from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QMenuBar,
    QMenu,
    QMessageBox,
    QFormLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from submit_button import submit_button


class RegisterPage(BaseAuthForm):
    def __init__(self, auth_manager):
        super().__init__(auth_manager, is_register=True)
        self.submit_button.setEnabled(email_valid and password_valid)

    def register_account(self):
        email = self.email_input.text()
        password = self.password_input.text()
