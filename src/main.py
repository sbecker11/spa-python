import sys
import logging
import traceback

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon

# Import configuration
from config.application_settings import ApplicationSettings

# Import main application window
from src.ui.main_window import UserManagementMainWindow

def configure_logging():
    """
    Configure application-wide logging
    """
    try:
        # Get configuration
        config = ApplicationSettings()
        
        # Configure logging
        log_level = config.get('logging.level', 'INFO')
        log_file = config.get('logging.file', 'app.log')
        
        # Setup logging
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename=log_file,
            filemode='a'
        )
        
        # Create logger
        logger = logging.getLogger(__name__)
        logger.info("Logging configured successfully")
        
        return logger
    except Exception as e:
        print(f"Error configuring logging: {e}")
        # Fallback to basic logging
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)

def exception_hook(exctype, value, tb):
    """
    Global exception handler
    
    Logs unhandled exceptions and shows user-friendly error message
    """
    # Log the full traceback
    logging.error("Uncaught exception", exc_info=(exctype, value, tb))
    
    # Create error message
    error_message = ''.join(traceback.format_exception(exctype, value, tb))
    
    # Show error dialog
    app = QApplication.instance()
    if app:
        QMessageBox.critical(
            None, 
            "Unexpected Error", 
            f"An unexpected error occurred:\n\n{error_message}"
        )
    
    # Call the default exception handler
    sys.__excepthook__(exctype, value, tb)

def main():
    """
    Main application entry point
    """
    try:
        # Configure logging
        logger = configure_logging()
        
        # Get application configuration
        config = ApplicationSettings()
        
        # Create application
        app = QApplication(sys.argv)
        
        # Set application metadata
        app.setApplicationName(config.get('app_name', 'User Management App'))
        app.setApplicationVersion(config.get('version', '1.0.0'))
        
        # Set global exception handler
        sys.excepthook = exception_hook
        
        # Create and show main window
        main_window = UserManagementMainWindow()
        
        # Set application icon
        try:
            icon = QIcon('resources/icons/app_icon.png')
            app.setWindowIcon(icon)
            main_window.setWindowIcon(icon)
        except Exception as e:
            logger.warning(f"Could not set application icon: {e}")
        
        # Show main window
        main_window.show()
        
        # Log application start
        logger.info("Application started successfully")
        
        # Run the application
        sys.exit(app.exec())
    
    except Exception as e:
        # Log any startup errors
        logging.critical(f"Fatal error during application startup: {e}", exc_info=True)
        
        # Show error to user
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setText("Application Startup Failed")
        error_dialog.setInformativeText(str(e))
        error_dialog.setWindowTitle("Startup Error")
        error_dialog.exec()
        
        sys.exit(1)

if __name__ == "__main__":
    main()