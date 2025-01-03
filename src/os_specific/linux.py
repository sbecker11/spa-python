from PyQt6.QtWidgets import QMessageBox

def linux_specific_function():
    QMessageBox.information(None, "Platform", "Running on Linux")
