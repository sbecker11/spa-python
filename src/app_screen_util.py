from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QCursor

class AppScreenUtil:
    """Utility class for handling screen-related operations."""
    
    @staticmethod
    def show_screen_geometries():
        """Print the geometries of all screens."""
        for index, screen in enumerate(QApplication.screens()):
            geometry = screen.geometry()
            print(f'Screen[{index}]: {geometry.width()}x{geometry.height()}')

    @staticmethod
    def move_to_screen(window, screen_index=0):
        """Move the window to the specified screen."""
        screens = QApplication.screens()
        if 0 <= screen_index < len(screens):
            screen = screens[screen_index]
            screen_geometry = screen.geometry()
            window.move(screen_geometry.x() + (screen_geometry.width() - window.width()) // 2,
                        screen_geometry.y() + (screen_geometry.height() - window.height()) // 2)
        else:
            print(f"Screen index {screen_index} is out of range. Using primary screen.")
            primary_screen = QApplication.primaryScreen()
            screen_geometry = primary_screen.geometry()
            window.move(screen_geometry.x() + (screen_geometry.width() - window.width()) // 2,
                        screen_geometry.y() + (screen_geometry.height() - window.height()) // 2)

    @staticmethod
    def get_invoked_screen_index(window):
        """Determine the screen index from which the application was invoked."""
        cursor_pos = QCursor.pos()
        screens = QApplication.screens()
        for index, screen in enumerate(screens):
            if screen.geometry().contains(cursor_pos):
                return index
        return 0  # Default to primary screen if not found
    