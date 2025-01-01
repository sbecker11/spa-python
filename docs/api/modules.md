# Application Modules Documentation

## Core Modules

### Authentication (`src/auth`)
- `authentication_service.py`: User authentication logic
  - Methods:
    - `validate_email(email)`
    - `validate_password(password)`
    - `register_account(email, password)`
    - `login(email, password)`

### Pages (`src/pages`)
- Manage different application views
  - `home_page.py`
  - `login_page.py`
  - `register_page.py`
  - `profile_page.py`

### Mixins (`src/mixins`)
- Reusable class components
  - `submit_button_handler.py`: Form submission logic

## Configuration
- `config/application_settings.py`: Centralized configuration management

## Packaging
- Tools for creating distributable application packages