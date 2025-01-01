import logging
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QMessageBox,
)
from PyQt6.QtCore import Qt


class BaseAuthForm(QWidget):
    """
    Base widget for authentication-related pages.

    This class provides a reusable form with email and password fields,
    including validation and submission logic.

    Attributes:
        auth_manager: Authentication manager for validation and account operations
        is_register: Flag to determine registration or login mode
    """

    def __init__(self, auth_manager, is_register=True):
        """
        Initialize the authentication form.

        Args:
            auth_manager: Authentication manager instance
            is_register (bool): True for registration, False for login
        """
        super().__init__()

        # Setup logging
        self.logger = logging.getLogger(__name__)

        # Store authentication mode
        self.is_register = is_register

        # Create main layout
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Email input
        self.email_input = QLineEdit()
        self.email_input.textChanged.connect(self.validate_email)
        self.email_error = QLabel()
        self.email_error.setStyleSheet("color: red")

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.textChanged.connect(self.validate_password)
        self.password_error = QLabel()
        self.password_error.setStyleSheet("color: red")

        # Add to form layout
        form_layout.addRow("Email:", self.email_input)
        form_layout.addWidget(self.email_error)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addWidget(self.password_error)

        # Submit button
        self.submit_button = QPushButton("Register" if is_register else "Login")
        self.submit_button.setEnabled(False)
        self.submit_button.clicked.connect(self.submit_form)

        # Add to main layout
        layout.addLayout(form_layout)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

        # Store auth manager
        self.auth_manager = auth_manager

    def validate_email(self) -> None:
        """
        Validate email input and update UI accordingly.
        """
        email = self.email_input.text()
        is_valid = self.auth_manager.validate_email(email)

        if not email:
            self.email_error.setText("")
            self.email_input.setStyleSheet("")
        elif not is_valid:
            self.email_error.setText("Invalid email format")
            self.email_input.setStyleSheet("border: 2px solid red")
        else:
            self.email_error.setText("")
            self.email_input.setStyleSheet("")

        self.update_submit_button()

    def validate_password(self) -> None:
        """
        Validate password input and update UI accordingly.
        """
        password = self.password_input.text()
        is_valid = self.auth_manager.validate_password(password)

        if not password:
            self.password_error.setText("")
            self.password_input.setStyleSheet("")
        elif not is_valid:
            self.password_error.setText(
                "Weak password. Requires 8+ chars, 1 upper, 1 lower, 1 digit, 1 special char"
            )
            self.password_input.setStyleSheet("border: 2px solid red")
        else:
            self.password_error.setText("")
            self.password_input.setStyleSheet("")

        self.update_submit_button()

    def update_submit_button(self) -> None:
        """
        Enable/disable submit button based on input validity.
        """
        email = self.email_input.text()
        password = self.password_input.text()

        email_valid = self.auth_manager.validate_email(email)
        password_valid = self.auth_manager.validate_password(password)

        self.submit_button.setEnabled(email_valid and password_valid)

    def submit_form(self) -> None:
        """
        Handle form submission based on mode (register or login).
        """
        email = self.email_input.text()
        password = self.password_input.text()

        try:
            if self.is_register:
                success, message = self.auth_manager.register_account(email, password)
            else:
                success, message = self.auth_manager.login(email, password)

            if success:
                # Success message
                QMessageBox.information(
                    self,
                    "Success",
                    f"{'Registration' if self.is_register else 'Login'} successful!",
                )
                # Clear inputs
                self.email_input.clear()
                self.password_input.clear()
            else:
                # Error message
                QMessageBox.warning(self, "Error", message)

        except Exception as e:
            # Log and show unexpected errors
            self.logger.error(f"Authentication error: {e}")
            QMessageBox.critical(
                self, "Critical Error", f"An unexpected error occurred: {e}"
            )
