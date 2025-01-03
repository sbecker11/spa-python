from PyQt6.QtWidgets import QMessageBox

def macos_specific_function():
    QMessageBox.information(None, "Platform", "Running on macOS")
