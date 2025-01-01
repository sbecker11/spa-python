import os
import shutil
import stat

class LinuxAppDirBuilder:
    """
    Create a Linux AppDir structure for AppImage packaging
    """
    def __init__(self, app_name, executable_path):
        """
        Initialize AppDir builder
        
        Args:
            app_name (str): Name of the application
            executable_path (str): Path to the executable
        """
        self.app_name = app_name
        self.executable_path = executable_path
        self.appdir_path = f"{app_name}.AppDir"

    def create_appdir_structure(self):
        """
        Create the complete AppDir structure
        """
        # Create base AppDir
        os.makedirs(self.appdir_path, exist_ok=True)
        
        # Create usr subdirectories
        usr_paths = [
            f"{self.appdir_path}/usr/bin",
            f"{self.appdir_path}/usr/lib",
            f"{self.appdir_path}/usr/share/applications",
            f"{self.appdir_path}/usr/share/icons/hicolor/256x256/apps"
        ]
        for path in usr_paths:
            os.makedirs(path, exist_ok=True)
        
        # Copy executable
        dest_executable = f"{self.appdir_path}/usr/bin/{self.app_name}"
        shutil.copy2(self.executable_path, dest_executable)
        # Make executable
        st = os.stat(dest_executable)
        os.chmod(dest_executable, st.st_mode | stat.S_IEXEC)

    def create_desktop_entry(self):
        """
        Create .desktop file for the application
        """
        desktop_file_path = f"{self.appdir_path}/usr/share/applications/{self.app_name}.desktop"
        desktop_content = f"""[Desktop Entry]
Type=Application
Name={self.app_name}
Exec={self.app_name}
Icon={self.app_name}
Categories=Utility;
"""
        with open(desktop_file_path, 'w') as f:
            f.write(desktop_content)

    def copy_icon(self, icon_path=None):
        """
        Copy application icon
        
        Args:
            icon_path (str, optional): Path to application icon
        """
        # Try to find an icon if not provided
        if not icon_path:
            possible_icons = [
                'app_icon.png', 
                'icon.png', 
                f'{self.app_name}.png'
            ]
            for icon in possible_icons:
                if os.path.exists(icon):
                    icon_path = icon
                    break
        
        if icon_path:
            dest_icon_path = f"{self.appdir_path}/usr/share/icons/hicolor/256x256/apps/{self.app_name}.png"
            shutil.copy2(icon_path, dest_icon_path)

    def create_apprun(self):
        """
        Create AppRun script
        """
        apprun_path = f"{self.appdir_path}/AppRun"
        apprun_content = f"""#!/bin/sh
HERE="$(dirname "$(readlink -f "${0}")")"
EXEC="${{HERE}}/usr/bin/{self.app_name}"
exec "$EXEC" "$@"
"""
        with open(apprun_path, 'w') as f:
            f.write(apprun_content)
        
        # Make AppRun executable
        st = os.stat(apprun_path)
        os.chmod(apprun_path, st.st_mode | stat.S_IEXEC)

    def build(self, icon_path=None):
        """
        Build complete AppDir structure
        
        Args:
            icon_path (str, optional): Path to application icon
        """
        self.create_appdir_structure()
        self.create_desktop_entry()
        self.copy_icon(icon_path)
        self.create_apprun()
        print(f"AppDir created at {self.appdir_path}")

def main():
    """
    Example usage
    """
    builder = LinuxAppDirBuilder("UserManagementApp", "dist/UserManagementApp")
    builder.build()

if __name__ == "__main__":
    main()