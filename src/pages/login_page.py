import logging
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt


class LoginPage:
    def login_account(self):
        """
        Attempt to log in with provided credentials

        Validates input, attempts authentication, and provides user feedback
        """
        # Setup logging
        logger = logging.getLogger(__name__)

        # Get input values
        email = self.email_input.text().strip()
        password = self.password_input.text()

        try:
            # Attempt to login
            success, message = self.auth_manager.login(email, password)

            if success:
                # Log successful login
                logger.info(f"Successful login for email: {email}")

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
                logger.warning(
                    f"Failed login attempt for email: {email}. Reason: {message}"
                )

                # Show error message
                QMessageBox.warning(
                    self, "Login Failed", message, QMessageBox.StandardButton.Ok
                )

        except Exception as e:
            # Log unexpected errors
            logger.error(f"Unexpected error during login: {e}")

            # Show critical error message
            QMessageBox.critical(
                self,
                "Login Error",
                "An unexpected error occurred. Please try again.",
                QMessageBox.StandardButton.Ok,
            )
