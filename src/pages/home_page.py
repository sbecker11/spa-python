import logging
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor


class HomePage(QWidget):
    def __init__(self):
        """
        Initialize the Home Page

        Creates a centered welcome message with styling
        """
        super().__init__()

        # Setup logging
        self.logger = logging.getLogger(__name__)

        # Create main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create frame for content
        content_frame = QFrame()
        content_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        content_frame.setLineWidth(1)
        layout.addWidget(content_frame)

        # Create frame layout
        frame_layout = QVBoxLayout(content_frame)

        # Create styled hello world label
        hello_label = QLabel("Welcome to User Management App")
        hello_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Customize label style
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        hello_label.setFont(font)

        # Set color
        palette = hello_label.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor(33, 33, 33))
        hello_label.setPalette(palette)

        # Add label to frame layout
        frame_layout.addWidget(hello_label)

        # Optional: Add a subtitle
        subtitle_label = QLabel("Navigate using the menu above")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setFont(QFont("Arial", 10))
        frame_layout.addWidget(subtitle_label)

        # Log page initialization
        self.logger.info("Home page initialized")

    def showEvent(self, event):
        """
        Called when the widget is shown

        Useful for logging or performing actions when the page becomes visible
        """
        super().showEvent(event)
        self.logger.info("Home page became visible")
