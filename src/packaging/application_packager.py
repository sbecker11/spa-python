import os
import sys
import logging
import subprocess
import shutil
from typing import Optional, List, Dict


class ApplicationPackager:
    """
    A comprehensive application packaging utility for cross-platform distribution.

    Supports creating standalone executables and platform-specific installers.
    """

    def __init__(
        self,
        app_name: str = "UserManagementApp",
        main_script: str = "main.py",
        icon_path: Optional[str] = None,
    ):
        """
        Initialize the application packager.

        Args:
            app_name (str): Name of the application
            main_script (str): Entry point script for the application
            icon_path (str, optional): Path to application icon
        """
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            filename="packaging.log",
        )
        self.logger = logging.getLogger(__name__)

        # Configuration
        self.app_name = app_name
        self.main_script = main_script
        self.icon_path = icon_path or self._find_default_icon()

        # Packaging configurations
        self.pyinstaller_options = self._get_default_pyinstaller_options()

    def _find_default_icon(self) -> Optional[str]:
        """
        Locate a default application icon.

        Returns:
            str or None: Path to the icon file
        """
        possible_icons = [
            "app_icon.ico",  # Windows
            "app_icon.icns",  # macOS
            "app_icon.png",  # Linux
            "icon.ico",
            "icon.icns",
            "icon.png",
        ]

        for icon in possible_icons:
            if os.path.exists(icon):
                return icon

        self.logger.warning("No default icon found")
        return None

    def _get_default_pyinstaller_options(self) -> List[str]:
        """
        Generate default PyInstaller options.

        Returns:
            List[str]: Default PyInstaller command options
        """
        options = [
            "--onefile",  # Single executable
            "--windowed",  # No console window
            f"--name={self.app_name}",
        ]

        # Add icon if available
        if self.icon_path:
            options.append(f"--icon={self.icon_path}")

        return options

    def create_package(self):
        """
        Create a standalone application package for the current platform.
        """
        try:
            # Run PyInstaller
            self._run_pyinstaller()

            # Create platform-specific installer
            self._create_platform_installer()

            self.logger.info("Application packaged successfully!")
            print("Application packaged successfully!")

        except subprocess.CalledProcessError as e:
            error_msg = f"Packaging failed: {e}"
            self.logger.error(error_msg)
            print(error_msg)

        except Exception as e:
            error_msg = f"An unexpected error occurred: {e}"
            self.logger.error(error_msg, exc_info=True)
            print(error_msg)

    def _run_pyinstaller(self):
        """
        Run PyInstaller to create the executable.
        """
        full_options = self.pyinstaller_options + [self.main_script]

        self.logger.info(f"Running PyInstaller with options: {full_options}")
        subprocess.run(
            ["pyinstaller"] + full_options, check=True, capture_output=True, text=True
        )

    def _create_platform_installer(self):
        """
        Create platform-specific installer based on the current OS.
        """
        platform_installers = {
            "darwin": self._create_mac_installer,
            "win32": self._create_windows_installer,
            "linux": self._create_linux_installer,
        }

        installer_func = platform_installers.get(sys.platform)
        if installer_func:
            installer_func()
        else:
            self.logger.warning(f"No installer support for platform: {sys.platform}")

    def _create_mac_installer(self):
        """
        Create macOS application bundle and disk image.
        """
        try:
            app_name = f"{self.app_name}.app"
            contents_dir = os.path.join(app_name, "Contents")
            macos_dir = os.path.join(contents_dir, "MacOS")
            resources_dir = os.path.join(contents_dir, "Resources")

            # Ensure directories exist
            os.makedirs(macos_dir, exist_ok=True)
            os.makedirs(resources_dir, exist_ok=True)

            # Copy executable and icon
            executable_path = os.path.join("dist", self.app_name)
            shutil.copy2(executable_path, os.path.join(macos_dir, self.app_name))

            if self.icon_path and self.icon_path.endswith(".icns"):
                shutil.copy2(
                    self.icon_path, os.path.join(resources_dir, "app_icon.icns")
                )

            # Create disk image
            subprocess.run(
                [
                    "hdiutil",
                    "create",
                    "-volname",
                    self.app_name,
                    "-srcfolder",
                    app_name,
                    "-ov",
                    f"{self.app_name}.dmg",
                ],
                check=True,
            )

            self.logger.info("Mac installer created successfully")

        except Exception as e:
            self.logger.error(f"Mac installer creation failed: {e}")
            raise

    def _create_windows_installer(self):
        """
        Create Windows installer using NSIS.
        Requires NSIS to be installed.
        """
        try:
            subprocess.run(
                [
                    "makensis",
                    f"/DPRODUCT_NAME={self.app_name}",
                    f"/DOUTPUT_FILE={self.app_name}_Installer.exe",
                    "installer.nsi",
                ],
                check=True,
            )
            self.logger.info("Windows installer created successfully")

        except Exception as e:
            self.logger.error(f"Windows installer creation failed: {e}")
            raise

    def _create_linux_installer(self):
        """
        Create Linux AppImage for portable distribution.
        """
        try:
            subprocess.run(
                [
                    "appimagetool",
                    f"{self.app_name}.AppDir",
                    f"{self.app_name}.AppImage",
                ],
                check=True,
            )
            self.logger.info("Linux AppImage created successfully")

        except Exception as e:
            self.logger.error(f"Linux installer creation failed: {e}")
            raise


def main():
    """
    Entry point for application packaging.
    """
    packager = ApplicationPackager()
    packager.create_package()


if __name__ == "__main__":
    main()
