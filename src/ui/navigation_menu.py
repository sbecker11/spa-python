from typing import Optional
from PyQt6.QtWidgets import QMenuBar, QMenu, QAction
from PyQt6.QtGui import QKeySequence, QIcon


class NavigationMenuBar(QMenuBar):
    """
    A configurable navigation menu bar for the user management application.

    Provides a standardized menu structure with common navigation actions.
    Supports optional keyboard shortcuts and icons.
    """

    def __init__(self, parent=None):
        """
        Initialize the navigation menu bar.

        Args:
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)

        # Create main navigation menu
        self._create_navigation_menu()

    def _create_navigation_menu(self):
        """
        Create and configure the navigation menu with standard actions.
        """
        # Create Navigation menu
        navigation_menu = self.addMenu("&Navigation")

        # Define menu actions with optional shortcuts and icons
        menu_actions = [
            {
                "label": "Home",
                "shortcut": QKeySequence("Ctrl+H"),
                "icon": self._get_icon("home_icon.png"),
                "attr_name": "home_action",
            },
            {
                "label": "About",
                "shortcut": QKeySequence("Ctrl+I"),
                "icon": self._get_icon("about_icon.png"),
                "attr_name": "about_action",
            },
            {
                "label": "Register",
                "shortcut": QKeySequence("Ctrl+R"),
                "icon": self._get_icon("register_icon.png"),
                "attr_name": "register_action",
            },
            {
                "label": "Login",
                "shortcut": QKeySequence("Ctrl+L"),
                "icon": self._get_icon("login_icon.png"),
                "attr_name": "login_action",
            },
            {
                "label": "Profile",
                "shortcut": QKeySequence("Ctrl+P"),
                "icon": self._get_icon("profile_icon.png"),
                "attr_name": "profile_action",
            },
            {
                "label": "Quit",
                "shortcut": QKeySequence("Ctrl+Q"),
                "icon": self._get_icon("quit_icon.png"),
                "attr_name": "quit_action",
            },
        ]

        # Create actions dynamically
        for action_config in menu_actions:
            action = navigation_menu.addAction(action_config["label"])

            # Set shortcut if provided
            if action_config["shortcut"]:
                action.setShortcut(action_config["shortcut"])

            # Set icon if provided
            if action_config["icon"]:
                action.setIcon(action_config["icon"])

            # Set as an attribute of the class
            setattr(self, action_config["attr_name"], action)

    def _get_icon(self, icon_path: Optional[str] = None):
        """
        Retrieve an icon for a menu action.

        Args:
            icon_path (str, optional): Path to the icon file. Defaults to None.

        Returns:
            QIcon or None: Icon for the menu action
        """
        if icon_path:
            try:
                return QIcon(icon_path)
            except Exception:
                # Log or handle icon loading failure
                return None
        return None

    def set_action_enabled(self, action_name: str, enabled: bool = True):
        """
        Enable or disable a specific menu action.

        Args:
            action_name (str): Name of the action to modify
            enabled (bool, optional): Enable or disable the action. Defaults to True.
        """
        try:
            action = getattr(self, action_name)
            action.setEnabled(enabled)
        except AttributeError:
            print(f"Action {action_name} not found")
