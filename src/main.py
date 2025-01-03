import os
import sys
from PyQt6.QtWidgets import QApplication

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print("PYTHONPATH:", sys.path)

from src.app_main_window import AppMainWindow

def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    
    # Check if running in headless mode
    if not QApplication.screens():
        print("This application requires a display. Exiting.")
        sys.exit(1)
    
    # Create the main window
    main_window = AppMainWindow(app)
    
    # Choose the screen
    screen_index = main_window.choose_screen()
    
    # Set the selected screen
    main_window.set_selected_screen(screen_index)
    
    # Show the main window
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()