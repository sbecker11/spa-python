# User Management Application

## Overview
A standalone desktop application for user registration, login, and profile management with robust security features.

## Features
- Responsive GUI with multiple pages
- Secure user registration
- Email and password validation
- Local account storage
- Profile management

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Installation

### Development Setup
1. Clone the repository
```bash
git clone https://github.com/yourusername/user-management-app.git
cd user-management-app
```

2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python main.py
```

### Building Standalone Package
```bash
pyinstaller --onefile --windowed main.py
```

## Password Validation Rules
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 digit
- At least 1 special character

## Security Notes
- Passwords are hashed using SHA-256
- Accounts stored locally in JSON format
- Email uniqueness enforced

## Troubleshooting
- Ensure Python and pip are correctly installed
- Check that all dependencies are installed
- Verify write permissions for account storage

## License
[Your License Here]

## Contributing
Contributions welcome. Please read CONTRIBUTING.md for details.
