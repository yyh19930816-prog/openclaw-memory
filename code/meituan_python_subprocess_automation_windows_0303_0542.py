#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Source: github.com/04AR/webcon_python_subprocess
Date: 2023-11-15
Description: Python subprocess management with virtual environment setup
"""

import os
import subprocess
import sys
from pathlib import Path


class VirtualEnvManager:
    """Handles virtual environment creation and management"""

    def __init__(self, path="."):
        self.path = Path(path).absolute()
        self.python = sys.executable
        self.venv_dir = self.path / "venv"

    def create_venv(self):
        """Create a new virtual environment"""
        print(f"Creating virtual environment at {self.venv_dir}")
        try:
            subprocess.run(
                [self.python, "-m", "venv", str(self.venv_dir)],
                check=True,
            )
            print("Virtual environment created successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to create virtual environment: {e}")
            return False

    def activate_command(self):
        """Return the activation command for the current OS"""
        if sys.platform == "win32":
            return str(self.venv_dir / "Scripts" / "activate")
        else:
            return f"source {self.venv_dir/'bin'/'activate'}"

    def install_requirements(self, req_file="requirements.txt"):
        """Install packages from requirements file"""
        req_path = self.path / req_file
        if not req_path.exists():
            print(f"No requirements file found at {req_path}")
            return False

        try:
            pip_exec = str(self.venv_dir / "bin" / "pip")
            if sys.platform == "win32":
                pip_exec = str(self.venv_dir / "Scripts" / "pip.exe")

            subprocess.run(
                [pip_exec, "install", "-r", str(req_path)],
                check=True,
            )
            print("Requirements installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install requirements: {e}")
            return False


def main():
    print("=== Virtual Environment Setup ===")
    
    # Initialize and create virtual environment
    venv_manager = VirtualEnvManager()
    if not venv_manager.create_venv():
        sys.exit(1)
    
    # Show activation command
    print("\nTo activate the virtual environment, run:")
    print(venv_manager.activate_command())
    
    # Install requirements if available
    if (Path(".") / "requirements.txt").exists():
        print("\nInstalling requirements...")
        if not venv_manager.install_requirements():
            sys.exit(1)
    
    print("\nSetup complete. Virtual environment is ready to use.")


if __name__ == "__main__":
    main()