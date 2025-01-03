from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from src.mixins.submit_button_mixin import SubmitButtonMixin

class RegisterPage(QWidget, SubmitButtonMixin):
    def __init__(self,auth_service):
        super().__init__()
        self.auth_service =auth_service

        # Create main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        # Create password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Create register button
        self.submit_button = QPushButton("Register")
        layout.addWidget(self.submit_button)

        # Setup submit button using mixin
        self._setup_submit_button()

    def _on_submit(self):
        """
        Specific implementation for register page
        """
        email = self.email_input.text().strip()
        password = self.password_input.text()

        try:
            # Attempt to register
            success, message = self.auth_service.register(email, password)

            if success:
                # Show success message
                QMessageBox.information(
                    self,
                    "Registration Successful",
                    "Your account has been created successfully!",
                    QMessageBox.StandardButton.Ok,
                )

                # Clear input fields
                self.email_input.clear()
                self.password_input.clear()
                self.submit_button.setEnabled(False)

                # Optionally switch to login page or perform additional actions
                # self.parent().switch_to_login_page()
            else:
                # Show error message
                QMessageBox.warning(
                    self, "Registration Failed", message, QMessageBox.StandardButton.Ok
                )

        except Exception as e:
            # Show critical error message
            QMessageBox.critical(
                self,
                "Registration Error",
                f"An unexpected error occurred: {e}",
                QMessageBox.StandardButton.Ok,
            )