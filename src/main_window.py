import logging
from PyQt6.QtWidgets import (
    QMainWindow, 
    QStackedWidget, 
    QVBoxLayout, 
    QWidget
)

# Import pages
from src.pages.home_page import HomePage
from src.pages.about_page import AboutPage
from src.pages.login_page import LoginPage
from src.pages.register_page import RegisterPage
from src.pages.profile_page import ProfilePage

# Import authentication manager
from src.auth.authentication_service import UserAuthenticator

# Import navigation menu
from src.ui.navigation_menu import NavigationMenuBar

class UserManagementMainWindow(QMainWindow):
    """
    Main application window managing page navigation and authentication
    """
    def __init__(self):
        """
        Initialize the main application window
        """
        super().__init__()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize authentication manager
        self.auth_manager = UserAuthenticator()
        
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
        
        self.logger.info("Main window initialized successfully")
    
    def _create_pages(self):
        """
        Create and add pages to the stacked widget
        """
        # Create page instances
        self.pages = {
            'home': HomePage(),
            'about': AboutPage(),
            'login': LoginPage(self.auth_manager),
            'register': RegisterPage(self.auth_manager),
            'profile': ProfilePage(self.auth_manager)
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