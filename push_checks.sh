#!/bin/bash

# Run Black for code formatting
black .

# Run Flake8 for linting
flake8 .

# Run Pylint for static analysis
pylint src/
