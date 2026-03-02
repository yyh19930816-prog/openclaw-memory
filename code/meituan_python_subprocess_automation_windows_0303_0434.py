#!/usr/bin/env python3
# Source: https://github.com/04AR/webcon_python_subprocess
# Date: 2023-10-15
# Description: Python subprocess management with virtual environment setup

import os
import sys
import subprocess
import platform
from typing import Optional, List


class VirtualEnvManager:
    """Manages Python virtual environments"""

    def __init__(self, venv_dir: str = ".venv"):
        """
        Initialize VirtualEnvManager with directory name
        :param venv_dir: Name of virtual environment directory
        """
        self.venv_dir = venv_dir

    def create_venv(self) -> bool:
        """
        Create a new virtual environment
        :return: True if successful, False otherwise
        """
        try:
            subprocess.run(
                [sys.executable, "-m", "venv", self.venv_dir],
                check=True,
                capture_output=True,
            )
            print(f"Virtual environment created in {self.venv_dir}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to create virtual environment: {e.stderr.decode().strip()}")
            return False

    def activate_venv(self) -> Optional[str]:
        """
        Activate the virtual environment
        :return: Activation command string if successful, None otherwise
        """
        if not os.path.exists(self.venv_dir):
            print(f"Virtual environment {self.venv_dir} does not exist")
            return None

        system = platform.system().lower()
        if system == "windows":
            activate_script = os.path.join(selfvenv_dir, "Scripts", "activate")
            activate_cmd = f"{activate_script}"
        else:
            activate_script = os.path.join(self.venv_dir, "bin", "activate")
            activate_cmd = f"source {activate_script}"

        if os.path.exists(activate_script):
            print(f"Run this command to activate:\n{activate_cmd}")
            return activate_cmd
        else:
            print(f"Activation script not found at {activate_script}")
            return None


class RequirementsInstaller:
    """Handles installation of Python requirements"""

    @staticmethod
    def install_requirements(file_path: str = "requirements.txt") -> bool:
        """
        Install packages from requirements file
        :param file_path: Path to requirements file
        :return: True if successful, False otherwise
        """
        if not os.path.exists(file_path):
            print(f"Requirements file {file_path} not found")
            return False

        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", file_path],
                check=True,
                capture_output=True,
            )
            print("Requirements installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install requirements: {e.stderr.decode().strip()}")
            return False


def main():
    """Main execution function"""
    print("Virtual Environment Setup Tool")

    # Initialize managers
    venv_manager = VirtualEnvManager()
    requirements_installer = RequirementsInstaller()

    # Create virtual environment
    if not venv_manager.create_venv():
        sys.exit(1)

    # Get activation command
    activate_cmd = venv_manager.activate_venv()
    if not activate_cmd:
        sys.exit(1)

    # Install requirements (would normally be separate step after activation)
    if not requirements_installer.install_requirements():
        print("Continuing without requirements installation")


if __name__ == "__main__":
    main()