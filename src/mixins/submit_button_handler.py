from PyQt6.QtWidgets import QPushButton

class SubmitButtonMixin:
    """
    A mixin class to handle submit button validation and connection
    """
    def _setup_submit_button(self):
        """
        Initial setup of submit button
        Ensures button is connected only once and sets initial state
        """
        # Disconnect any existing connections to prevent multiple calls
        try:
            self.submit_button.clicked.disconnect()
        except TypeError:
            # No existing connections, which is fine
            pass

        # Connect validation methods
        self.email_input.textChanged.connect(self.update_submit_button)
        self.password_input.textChanged.connect(self.update_submit_button)

        # Connect submit action
        self.submit_button.clicked.connect(self._on_submit)

        # Initial button state
        self.update_submit_button()

    def update_submit_button(self):
        """
        Update submit button's enabled state based on input validation
        """
        email = self.email_input.text()
        password = self.password_input.text()

        # Validate inputs
        email_valid = self.auth_manager.validate_email(email)
        password_valid = self.auth_manager.validate_password(password)

        # Enable/disable button based on validation
        self.submit_button.setEnabled(email_valid and password_valid)

    def _on_submit(self):
        """
        Default submit method to be overridden by specific page implementations
        """
        raise NotImplementedError(
            "Subclasses must implement the _on_submit method"
        )

# Example usage in a specific page class
class LoginPage(QWidget, SubmitButtonMixin):
    def __init__(self, auth_manager):
        super().__init__()
        self.auth_manager = auth_manager
        
        # Setup UI components (email_input, password_input, submit_button)
        self._setup_submit_button()  # From mixin

    def _on_submit(self):
        """
        Specific implementation for login page
        """
        email = self.email_input.text()
        password = self.password_input.text()

        # Attempt login
        success, message = self.auth_manager.login(email, password)
        
        if success:
            # Handle successful login
            QMessageBox.information(self, "Login", "Login successful!")
        else:
            # Handle login failure
            QMessageBox.warning(self, "Login Failed", message)