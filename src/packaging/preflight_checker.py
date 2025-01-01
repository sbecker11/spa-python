import os
import sys
import shutil
import subprocess
import platform

class PackagerPreflightChecker:
    """
    Perform comprehensive pre-packaging checks
    """
    def __init__(self, app_name, main_script):
        """
        Initialize preflight checker
        
        Args:
            app_name (str): Name of the application
            main_script (str): Main script to be packaged
        """
        self.app_name = app_name
        self.main_script = main_script
        self.errors = []
        self.warnings = []

    def check_python_version(self):
        """
        Verify Python version compatibility
        """
        min_version = (3, 8)
        current_version = sys.version_info
        
        if current_version < min_version:
            self.errors.append(
                f"Python version {'.'.join(map(str, current_version[:3]))} is too low. "
                f"Minimum required: {'.'.join(map(str, min_version))}"
            )
        return len(self.errors) == 0

    def check_required_dependencies(self):
        """
        Check for required packaging tools
        """
        dependencies = {
            "darwin": ["pyinstaller", "hdiutil"],
            "win32": ["pyinstaller", "makensis"],
            "linux": ["pyinstaller", "appimagetool"]
        }

        platform_deps = dependencies.get(sys.platform, [])
        
        for dep in platform_deps:
            try:
                subprocess.run(
                    [dep, "--version"], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    check=True
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.errors.append(f"Required dependency '{dep}' not found")
        
        return len(self.errors) == 0

    def check_main_script(self):
        """
        Verify main script exists and is readable
        """
        if not os.path.exists(self.main_script):
            self.errors.append(f"Main script {self.main_script} not found")
        elif not os.access(self.main_script, os.R_OK):
            self.errors.append(f"Main script {self.main_script} is not readable")
        
        return len(self.errors) == 0

    def check_disk_space(self, min_space_mb=500):
        """
        Check available disk space
        
        Args:
            min_space_mb (int): Minimum required free space in MB
        """
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Get free space
        total, used, free = shutil.disk_usage(current_dir)
        free_mb = free / (1024 * 1024)
        
        if free_mb < min_space_mb:
            self.warnings.append(
                f"Low disk space: {free_mb:.2f} MB free. "
                f"Recommended minimum: {min_space_mb} MB"
            )
        
        return free_mb >= min_space_mb

    def check_icon(self):
        """
        Check for application icon
        """
        icon_extensions = {
            "darwin": [".icns"],
            "win32": [".ico"],
            "linux": [".png"]
        }
        
        possible_icons = [
            f"app_icon{ext}" for ext in icon_extensions.get(sys.platform, [".png"])
        ]
        
        icon_found = any(os.path.exists(icon) for icon in possible_icons)
        
        if not icon_found:
            self.warnings.append(
                f"No platform-specific icon found. "
                f"Looked for: {', '.join(possible_icons)}"
            )
        
        return icon_found

    def run_preflight_checks(self):
        """
        Run all preflight checks
        
        Returns:
            bool: True if all checks pass, False otherwise
        """
        # Reset errors and warnings
        self.errors = []
        self.warnings = []

        # Run individual checks
        checks = [
            self.check_python_version,
            self.check_required_dependencies,
            self.check_main_script,
            self.check_disk_space,
            self.check_icon
        ]

        # Perform checks
        all_passed = all(check() for check in checks)

        # Print results
        if self.errors:
            print("Packaging Errors:")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print("Packaging Warnings:")
            for warning in self.warnings:
                print(f"  - {warning}")

        return all_passed

def main():
    """
    Example usage of preflight checker
    """
    checker = PackagerPreflightChecker("UserManagementApp", "main.py")
    
    if checker.run_preflight_checks():
        print("All preflight checks passed. Ready to package!")
    else:
        print("Packaging aborted due to errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()