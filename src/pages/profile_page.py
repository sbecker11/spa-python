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
from submit_button import *


class ProfilePage(BaseAuthForm):
    def __init__(self, auth_manager):
        super().__init__(auth_manager, is_register=False)

        # Change button text and connect to save profile
        self.submit_button.setText("Save Profile")
        self.submit_button.setEnabled(False)

        # Track original email for updates
        self.original_email = ""

        # Add listeners to detect changes
        self.email_input.textChanged.connect(self.check_changes)
        self.password_input.textChanged.connect(self.check_changes)

    def load_profile(self, email):
        """
        Load existing profile details
        """
        self.original_email = email
        self.email_input.setText(email)
        self.submit_button.setText("Save Profile")
        self.submit_button.setEnabled(False)

    def check_changes(self):
        """
        Check if profile details have changed
        """
        current_email = self.email_input.text()
        current_password = self.password_input.text()

        # Enable save button if fields are valid and changed
        email_valid = self.auth_manager.validate_email(current_email)
        password_valid = (
            self.auth_manager.validate_password(current_password)
            if current_password
            else True
        )

        is_changed = current_email != self.original_email or current_password != ""

        self.submit_button.setEnabled(email_valid and password_valid and is_changed)

    def save_profile(self):
        """
        Save updated profile details
        """
        new_email = self.email_input.text()
        new_password = self.password_input.text()

        # If no password provided, keep the existing one
        if not new_password:
            success, message = self.auth_manager.update_account(
                self.original_email,
                new_email,
                "existing_password",  # Placeholder to keep existing password
            )
        else:
            success, message = self.auth_manager.update_account(
                self.original_email, new_email, new_password
            )

        if success:
            QMessageBox.information(
                self, "Profile Updated", "Your profile has been updated successfully!"
            )
            # Update original email
            self.original_email = new_email
            # Clear password field
            self.password_input.clear()
            self.submit_button.setEnabled(False)
        else:
            QMessageBox.warning(self, "Update Failed", message)
