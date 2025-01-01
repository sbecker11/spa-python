import os
import pytest
import tempfile

# Import the authentication service
from src.auth.authentication_service import UserAuthenticator

class TestUserAuthenticator:
    @pytest.fixture
    def temp_storage(self):
        """
        Create a temporary storage file for each test
        """
        with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.json') as temp_file:
            temp_file_path = temp_file.name
        
        yield temp_file_path
        
        # Cleanup
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

    def test_email_validation(self, temp_storage):
        """
        Test email validation
        """
        auth = UserAuthenticator(storage_path=temp_storage)
        
        # Valid email tests
        valid_emails = [
            'user@example.com',
            'john.doe@company.co.uk',
            'first_last@domain.org'
        ]
        
        for email in valid_emails:
            assert auth.validate_email(email) is True, f"Failed to validate {email}"
        
        # Invalid email tests
        invalid_emails = [
            'invalid-email',
            'user@',
            '@domain.com',
            'user@domain',
            'user@.com'
        ]
        
        for email in invalid_emails:
            assert auth.validate_email(email) is False, f"Incorrectly validated {email}"

    def test_password_validation(self, temp_storage):
        """
        Test password validation
        """
        auth = UserAuthenticator(storage_path=temp_storage)
        
        # Valid password tests
        valid_passwords = [
            'Strong1Pass!',
            'Secure2023@Pass',
            'Complex3Pwd#'
        ]
        
        for pwd in valid_passwords:
            assert auth.validate_password(pwd) is True, f"Failed to validate {pwd}"
        
        # Invalid password tests
        invalid_passwords = [
            'short',
            'ALLUPPERCASE',
            'alllowercase',
            '12345678',
            'NoSpecialChar1'
        ]
        
        for pwd in invalid_passwords:
            assert auth.validate_password(pwd) is False, f"Incorrectly validated {pwd}"

    def test_account_registration(self, temp_storage):
        """
        Test account registration process
        """
        auth = UserAuthenticator(storage_path=temp_storage)
        
        # Successful registration
        email = 'newuser@example.com'
        password = 'ValidStrong1Pass!'
        
        success, account_id = auth.register_account(email, password)
        assert success is True, "Registration failed"
        assert account_id is not None, "No account ID generated"
        
        # Duplicate registration attempt
        success, message = auth.register_account(email, password)
        assert success is False, "Allowed duplicate registration"
        assert "already registered" in message.lower()

    def test_login_process(self, temp_storage):
        """
        Test login authentication
        """
        auth = UserAuthenticator(storage_path=temp_storage)
        
        # Setup test account
        email = 'testuser@example.com'
        password = 'ValidStrong2Pass!'
        auth.register_account(email, password)
        
        # Successful login
        success, account_id = auth.login(email, password)
        assert success is True, "Login failed for valid credentials"
        assert account_id is not None, "No account ID returned on login"
        
        # Failed login attempts
        invalid_email = 'nonexistent@example.com'
        invalid_password = 'WrongPassword1!'
        
        # Wrong email
        success, message = auth.login(invalid_email, password)
        assert success is False, "Login succeeded with non-existent email"
        assert "not found" in message.lower()
        
        # Wrong password
        success, message = auth.login(email, invalid_password)
        assert success is False, "Login succeeded with incorrect password"
        assert "incorrect password" in message.lower()

def main():
    """
    Run tests directly
    """
    pytest.main([__file__])

if __name__ == '__main__':
    main()