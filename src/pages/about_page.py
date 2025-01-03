import sys
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
print("PYTHONPATH:", sys.path)

class AboutPage(QWidget):
    """
    AboutPage displays information about the application.
    """

    def __init__(self):
        super().__init__()

        # Create layout
        layout = QVBoxLayout()

        # Create image label
        image_label = QLabel()
        image_path = self.get_image_path()  # Get OS-specific image path
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            image_label.setPixmap(
                pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio)
            )
        else:
            image_label.setText("Image not found")
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(image_label)
        self.setLayout(layout)

    def get_image_path(self):
        """
        Get the image path based on the operating system.
        """
        if platform.system() == 'Windows':
            return "images/windows/couple_image.png"
        elif platform.system() == 'Darwin':
            return "images/macos/couple_image.png"
        elif platform.system() == 'Linux':
            return "images/linux/couple_image.png"
        else:
            return "images/default/couple_image.png"