import os
import json
import re
import hashlib
import uuid
import logging
from datetime import datetime, timedelta


class AuthService:
    """ handles userauth """
    def __init__(self, storage_path="accounts.json", max_login_attempts=5):
        """
        Initialize theauth service with a file-based storage

        Args:
            storage_path (str): Path to the accounts storage file
            max_login_attempts (int): Maximum failed login attempts before lockout
        """
        # Setup logging
        self.logger = logging.getLogger(__name__)

        # Configuration
        self.storage_path = storage_path
        self.MAX_LOGIN_ATTEMPTS = max_login_attempts

        # Load accounts
        self.accounts = self.load_accounts()

    def load_accounts(self):
        """
        Load accounts from the storage file

        Returns:
            dict: Loaded accounts or empty dictionary
        """
        try:
            if not os.path.exists(self.storage_path):
                self.logger.info("No existing accounts file. Creating new.")
                return {}

            with open(self.storage_path, "r") as f:
                accounts = json.load(f)
                self.logger.info(f"Loaded {len(accounts)} accounts")
                return accounts
        except (IOError, json.JSONDecodeError) as e:
            self.logger.error(f"Error loading accounts: {e}")
            return {}

    def save_accounts(self):
        """
        Save accounts to the storage file with error handling
        """
        try:
            with open(self.storage_path, "w") as f:
                json.dump(self.accounts, f, indent=4)
            self.logger.info("Accounts saved successfully")
        except IOError as e:
            self.logger.error(f"Error saving accounts: {e}")

    def validate_email(self, email):
        """
        Validate email format

        Args:
            email (str): Email to validate

        Returns:
            bool: True if email is valid, False otherwise
        """
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_regex, email) is not None

    def validate_password(self, password):
        """
        Validate password strength

        Args:
            password (str): Password to validate

        Returns:
            bool: True if password meets requirements, False otherwise
        """
        # Check length
        if len(password) < 8:
            return False

        # Check for complexity
        criteria = [
            re.search(r"[A-Z]", password),  # Uppercase
            re.search(r"[a-z]", password),  # Lowercase
            re.search(r"\d", password),  # Digit
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password),  # Special character
        ]

        return all(criteria)

    def email_exists(self, email):
        """
        Check if email already exists in accounts

        Args:
            email (str): Email to check

        Returns:
            bool: True if email exists, False otherwise
        """
        return email in self.accounts

    def register_account(self, email, password):
        """
        Register a new account

        Args:
            email (str): User's email
            password (str): User's password

        Returns:
            tuple: (Success boolean, Message or Account ID)
        """
        # Validate email and password
        if not self.validate_email(email):
            self.logger.warning(f"Invalid email format: {email}")
            return False, "Invalid email format"

        if not self.validate_password(password):
            self.logger.warning("Password does not meet strength requirements")
            return False, "Password does not meet strength requirements"

        # Check if email already exists
        if self.email_exists(email):
            self.logger.warning(f"Email already registered: {email}")
            return False, "Email already registered"

        # Generate unique ID and hash password
        account_id = str(uuid.uuid4())
        hashed_password = self._hash_password(password)

        # Store account
        self.accounts[email] = {
            "id": account_id,
            "password": hashed_password,
            "created_at": datetime.now().isoformat(),
            "login_attempts": 0,
            "locked_until": None,
        }

        # Save accounts
        self.save_accounts()

        self.logger.info(f"Account registered: {email}")
        return True, account_id

    def login(self, email, password):
        """
        Attempt to log in with email and password

        Args:
            email (str): User's email
            password (str): User's password

        Returns:
            tuple: (Success boolean, Message or Account ID)
        """
        # Check if email exists
        if not self.email_exists(email):
            self.logger.warning(f"Login attempt with non-existent email: {email}")
            return False, "Email not found"

        account = self.accounts[email]

        # Check if account is locked
        if account.get("locked_until"):
            locked_until = datetime.fromisoformat(account["locked_until"])
            if datetime.now() < locked_until:
                self.logger.warning(f"Login attempt on locked account: {email}")
                return False, f"Account locked. Try again after {locked_until}"

        # Verify password
        stored_hashed_password = account["password"]
        input_hashed_password = self._hash_password(password)

        if stored_hashed_password != input_hashed_password:
            # Increment login attempts
            account["login_attempts"] = account.get("login_attempts", 0) + 1

            # Lock account after max attempts
            if account["login_attempts"] >= self.MAX_LOGIN_ATTEMPTS:
                lock_duration = timedelta(minutes=15)
                account["locked_until"] = (datetime.now() + lock_duration).isoformat()
                self.logger.warning(
                    f"Account locked due to multiple failed attempts: {email}"
                )
                self.save_accounts()
                return False, "Too many failed attempts. Account locked for 15 minutes."

            self.save_accounts()
            self.logger.warning(f"Incorrect password for email: {email}")
            return False, "Incorrect password"

        # Reset login attempts on successful login
        account["login_attempts"] = 0
        account["locked_until"] = None
        self.save_accounts()

        self.logger.info(f"Successful login: {email}")
        return True, account["id"]

    def update_account(self, old_email, new_email, new_password):
        """
        Update account details

        Args:
            old_email (str): Current email
            new_email (str): New email
            new_password (str): New password

        Returns:
            tuple: (Success boolean, Message or Account ID)
        """
        # Validate new email and password
        if not self.validate_email(new_email):
            self.logger.warning(f"Invalid new email format: {new_email}")
            return False, "Invalid email format"

        if not self.validate_password(new_password):
            self.logger.warning("New password does not meet strength requirements")
            return False, "Password does not meet strength requirements"

        # Check if new email is already in use (by a different account)
        if new_email != old_email and self.email_exists(new_email):
            self.logger.warning(f"Email already registered: {new_email}")
            return False, "Email already registered"

        # Remove old email entry if changed
        if old_email != new_email:
            account_data = self.accounts.pop(old_email)
        else:
            account_data = self.accounts[old_email]

        # Update with new details
        hashed_password = self._hash_password(new_password)
        account_data["password"] = hashed_password

        # Store under new email
        self.accounts[new_email] = account_data
        self.save_accounts()

        self.logger.info(f"Account updated: {old_email} -> {new_email}")
        return True, account_data["id"]

    def _hash_password(self, password):
        """
        Hash password using SHA-256

        Args:
            password (str): Password to hash

        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
