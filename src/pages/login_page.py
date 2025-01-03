import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from src.mixins.submit_button_mixin import SubmitButtonMixin

class LoginPage(QWidget, SubmitButtonMixin):
    def __init__(self,auth_service):
        """
        Initialize the Login Page

        Creates the login form and sets up the layout
        """
        super().__init__()

        self.auth_service =auth_service

        # Setup logging
        self.logger = logging.getLogger(__name__)

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

        # Create login button
        self.submit_button = QPushButton("Login")
        layout.addWidget(self.submit_button)

        # Setup submit button using mixin
        self._setup_submit_button()

    def _on_submit(self):
        """
        Specific implementation for login page
        """
        email = self.email_input.text().strip()
        password = self.password_input.text()

        try:
            # Attempt to login
            success, message = self.auth_service.login(email, password)

            if success:
                # Log successful login
                self.logger.info(f"Successful login for email: {email}")

                # Show success message
                QMessageBox.information(
                    self,
                    "Login Successful",
                    "You have logged in successfully!",
                    QMessageBox.StandardButton.Ok,
                )

                # Clear input fields
                self.email_input.clear()
                self.password_input.clear()

                # Optionally switch to profile page or perform additional actions
                # self.parent().switch_to_profile_page()
            else:
                # Log failed login attempt
                self.logger.warning(
                    f"Failed login attempt for email: {email}. Reason: {message}"
                )

                # Show error message
                QMessageBox.warning(
                    self, "Login Failed", message, QMessageBox.StandardButton.Ok
                )

        except Exception as e:
            # Log unexpected errors
            self.logger.error(f"Unexpected error during login: {e}")

            # Show critical error message
            QMessageBox.critical(
                self,
                "Login Error",
                "An unexpected error occurred. Please try again.",
                QMessageBox.StandardButton.Ok,
            )