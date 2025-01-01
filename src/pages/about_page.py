from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, AlignmentFlag
from PyQt6.QtGui import QPixmap


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
        image_path = "couple_image.png"  # Placeholder image
        if not QPixmap(image_path).isNull():
            pixmap.scaled(400, 300, AspectRatioMode.KeepAspectRatio)
            image_label.setPixmap(
                pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio)
            )
        else:
            image_label.setText("Image not found")
            image_label.setAlignment(AlignmentFlag.AlignCenter)
            image_label.setAlignment(AlignmentFlag.AlignCenter)
            self.setLayout(layout)

        # def set_image(self, image_path) -> NotImplementedError:
        #     """
        #     Sets the image in the QLabel.
        #     """
        #     image_label = self.findChild(QLabel)
        #     if not QPixmap(image_path).isNull():
        #         image_label.setPixmap(
        #             QPixmap(image_path).scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio)
        #         )
        #     else:
        #         image_label.setText("Image not found")

        # def clear_image(self) -> NotImplementedError:
        #     """
        #     Clears the image in the QLabel.
        #     """
        #     image_label = self.findChild(QLabel)
        #     image_label.clear()
        #     layout.addWidget(image_label)

        #     self.setLayout(layout)
