# Testing Guide

## Running Tests

### Entire Test Suite
```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Show coverage
pytest --cov=src

Specific Test Modules
bashCopy# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::TestauthService::test_email_validation
Writing Tests

Use pytest
Place tests in tests/ directory
Follow naming convention: test_*.py
Use descriptive test method names

Test Categories

Unit Tests

Test individual functions/methods
Isolated from external dependencies


Integration Tests

Test interactions between components
Verify system works as a whole


Authentication Tests

Validate email formats
Check password strength
Test login scenarios




