#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Source: GitHub repo 04AR/webcon_python_subprocess
Date: Current date
Description: Python script demonstrating virtual environment setup and package installation
             using subprocess module for automation.
"""

import subprocess
import sys
import platform
from pathlib import Path


def create_venv(venv_path="."):
    """Create a Python virtual environment."""
    try:
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        print(f"Virtual environment created successfully at {venv_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False


def activate_venv(venv_path="."):
    """Activate the virtual environment."""
    system = platform.system()
    activate_script = ""
    
    try:
        if system == "Windows":
            activate_script = str(Path(venv_path) / "Scripts" / "activate.bat")
            subprocess.run(f"cmd /k {activate_script}", shell=True, check=True)
        else:  # Linux/MacOS
            activate_script = str(Path(venv_path) / "bin" / "activate")
            subprocess.run(f"source {activate_script}", shell=True, check=True)
        
        print("Virtual environment activated")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error activating virtual environment: {e}")
        return False


def install_requirements(req_file="requirements.txt"):
    """Install packages from requirements.txt."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file], check=True)
        print(f"Requirements installed from {req_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False
    except FileNotFoundError:
        print(f"Requirements file {req_file} not found")
        return False


def main():
    """Main function to automate setup process."""
    print("Starting project setup...")
    
    if not create_venv():
        return
    
    if not activate_venv():
        return
    
    if not install_requirements():
        print("Continuing without requirements installation")


if __name__ == "__main__":
    main()