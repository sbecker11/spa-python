from PyQt6.QtWidgets import QMessageBox

def windows_specific_function():
    QMessageBox.information(None, "Platform", "Running on Windows")
