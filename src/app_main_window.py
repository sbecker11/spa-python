import sys
import logging
import platform
from PyQt6.QtWidgets import (
    QMainWindow, 
    QStackedWidget, 
    QVBoxLayout, 
    QWidget,
    QMessageBox,
    QInputDialog,
    QApplication
)
from src.app_signal_util import AppSignalUtil
from src.app_screen_util import AppScreenUtil

# Import pages
from src.pages.home_page import HomePage
from src.pages.about_page import AboutPage
from src.pages.login_page import LoginPage
from src.pages.register_page import RegisterPage
from src.pages.profile_page import ProfilePage

# Importauth service
from auth.auth_service import AuthService

# Import navigation menu
from src.ui.navigation_menu import NavigationMenuBar

# OS-specific imports
if platform.system() == 'Windows':
    import pywin32
elif platform.system() == 'Darwin':
    import dmgbuild
elif platform.system() == 'Linux':
    import appimagetool

class AppMainWindow(QMainWindow):
    """
    Main application window managing page navigation,auth, and signal handling
    """
    def __init__(self, app):
        """
        Initialize the main application window
        """
        super().__init__()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Initializeauth service
        self.auth_service = AuthService()
        
        # Configure main window
        self.setWindowTitle("User Management Application")
        self.resize(800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        
        # Create navigation menu bar
        self.menu_bar = NavigationMenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        # Create stacked widget for page management
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # Create pages
        self._create_pages()
        
        # Setup menu connections
        self._setup_menu_connections()
        
        # Set initial page
        self.show_home_page()
        
        # Handle OS-specific functionality
        self.handle_os_specific_functionality()
        
        # Initialize signal handling
        self.signal_util = AppSignalUtil(app)
        
        self.logger.info("Main window initialized successfully")
    
    def _create_pages(self):
        """
        Create and add pages to the stacked widget
        """
        # Create page instances
        self.pages = {
            'home': HomePage(),
            'about': AboutPage(),
            'login': LoginPage(self.auth_service),
            'register': RegisterPage(self.auth_service),
            'profile': ProfilePage(self.auth_service)
        }
        
        # Add pages to stacked widget
        for page in self.pages.values():
            self.stacked_widget.addWidget(page)
    
    def _setup_menu_connections(self):
        """
        Connect menu actions to page switching methods
        """
        # Define menu action to page method mapping
        menu_page_map = {
            'home_action': self.show_home_page,
            'about_action': self.show_about_page,
            'login_action': self.show_login_page,
            'register_action': self.show_register_page,
            'profile_action': self.show_profile_page,
            'quit_action': self.close
        }
        
        # Connect actions to methods
        for action_name, method in menu_page_map.items():
            getattr(self.menu_bar, action_name).triggered.connect(method)
    
    def _switch_page(self, page_name):
        """
        Switch to the specified page
        
        Args:
            page_name (str): Name of the page to switch to
        """
        try:
            page = self.pages[page_name]
            self.stacked_widget.setCurrentWidget(page)
            self.logger.info(f"Switched to {page_name} page")
        except Exception as e:
            self.logger.error(f"Error switching to page {page_name}: {e}")
    
    def show_home_page(self):
        """Show home page"""
        self._switch_page('home')
    
    def show_about_page(self):
        """Show about page"""
        self._switch_page('about')
    
    def show_login_page(self):
        """Show login page"""
        self._switch_page('login')
    
    def show_register_page(self):
        """Show registration page"""
        self._switch_page('register')
    
    def show_profile_page(self):
        """Show profile page"""
        self._switch_page('profile')
    
    def handle_os_specific_functionality(self):
        """Handle OS-specific functionality"""
        if platform.system() == 'Windows':
            self.logger.info("Running on Windows")
            # Windows-specific code
        elif platform.system() == 'Darwin':
            self.logger.info("Running on macOS")
            # macOS-specific code
        elif platform.system() == 'Linux':
            self.logger.info("Running on Linux")
            self.linux_specific_function()
    
    def linux_specific_function(self):
        """Linux-specific functionality"""
        QMessageBox.information(self, "Platform", "Running on Linux")

    def choose_screen(self):
        """Prompt the user to choose a screen."""
        screens = QApplication.screens()
        invoked_screen_index = AppScreenUtil.get_invoked_screen_index(self)
        
        screen_list = []
        for index, screen in enumerate(screens):
            geometry = screen.geometry()
            prefix = "*" if index == invoked_screen_index else " "
            screen_list.append(f"{prefix} {index + 1}) Display {index + 1} ({geometry.width()}x{geometry.height()})")
        
        screen_list.append("q) Quit")
        
        screen_choice = f"App is being invoked from screen index: {invoked_screen_index}\n"
        screen_choice += "\n".join(screen_list)
        screen_choice += "\nEnter your choice (1-{}) or q to quit [default: {}]: ".format(len(screens), invoked_screen_index + 1)
        
        choice, ok = QInputDialog.getText(self, "Choose Screen", screen_choice)
        
        if ok and choice.isdigit():
            screen_index = int(choice) - 1
            if 0 <= screen_index < len(screens):
                return screen_index
        elif choice.lower() == 'q':
            print("No screen selected. Exiting application.")
            sys.exit(0)
        
        return invoked_screen_index

    def set_selected_screen(self, screen_index):
        """Set the selected screen and move the window to that screen."""
        AppScreenUtil.move_to_screen(self, screen_index)