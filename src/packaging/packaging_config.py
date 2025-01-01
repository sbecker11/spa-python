import os
import json
import platform
from typing import Dict, Any, Optional

class PackagingConfig:
    """
    Manage packaging configuration with support for 
    platform-specific and environment-specific settings
    """
    
    DEFAULT_CONFIG = {
        "app_name": "UserManagementApp",
        "version": "1.0.0",
        "main_script": "main.py",
        "icon_path": None,
        "platforms": {
            "darwin": {
                "installer_type": "dmg",
                "extra_files": [],
                "pyinstaller_options": [
                    "--osx-bundle-identifier=com.yourcompany.usermanagement"
                ]
            },
            "win32": {
                "installer_type": "nsis",
                "extra_files": ["README.txt", "LICENSE"],
                "pyinstaller_options": [
                    "--uac-admin"
                ]
            },
            "linux": {
                "installer_type": "appimage",
                "extra_files": [],
                "pyinstaller_options": [
                    "--linux-onefile-icon=app_icon.png"
                ]
            }
        },
        "packaging": {
            "include_dirs": ["resources", "data