# Developer Setup Guide

## Environment Setup

### Python Version
- Recommended: Python 3.8+
- Verify Python version:
```bash
python --version

Virtual Environment
bashCopy# Create virtual environment
python -m venv venv

# Activate
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
Install Dependencies
bashCopy# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e .[dev]

IDE Configuration
VSCode

Install Python extension
Select interpreter from venv
Install recommended extensions:

Python
PyQt
Pylance
Flake8



PyCharm

Open project
Configure Python interpreter
Install recommended plugins

