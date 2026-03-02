#!/usr/bin/env python3
"""
Python Subprocess Command Execution Script
Source: github.com/04AR/webcon_python_subprocess
Date: October 2023
Description: Creates virtual environment and installs requirements via subprocess
"""

import subprocess
import sys
import os
from pathlib import Path

def create_virtual_env(env_path="."):
    """
    Create Python virtual environment in specified directory
    
    Args:
        env_path (str): Path where virtual env should be created
    """
    try:
        # Create virtual environment using Python's built-in venv module
        subprocess.run([sys.executable, "-m", "venv", env_path], check=True)
        print(f"Virtual environment created successfully at {env_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create virtual environment: {e}")
        sys.exit(1)

def activate_virtual_env(env_path="."):
    """
    Activate the virtual environment based on OS
    
    Args:
        env_path (str): Path where virtual env exists
    """
    activation_script = ""
    
    if sys.platform == "win32":
        activation_script = str(Path(env_path) / "Scripts" / "activate.bat")
    else:  # Unix-like systems
        activation_script = str(Path(env_path) / "bin" / "activate")
    
    try:
        print(f"Run this command to activate virtual environment:")
        print(f"# Windows: {activation_script}")
        print(f"# Unix: source {activation_script}")
    except Exception as e:
        print(f"Error identifying activation script: {e}")

def install_requirements(req_file="requirements.txt"):
    """
    Install Python packages from requirements file
    
    Args:
        req_file (str): Path to requirements.txt file
    """
    if not os.path.exists(req_file):
        print(f"Requirements file {req_file} not found")
        return
    
    try:
        # Use pip from the virtual environment
        pip_executable = "pip"
        if sys.platform == "win32":
            pip_executable = str(Path("venv") / "Scripts" / "pip.exe")
        else:
            pip_executable = str(Path("venv") / "bin" / "pip")
            
        subprocess.run(
            [pip_executable, "install", "-r", req_file], 
            check=True
        )
        print("Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")
        sys.exit(1)

def main():
    """Main function to setup project environment"""
    print("\nStarting project environment setup...")
    
    # Step 1: Create virtual environment
    print("\nCreating virtual environment...")
    create_virtual_env("venv")
    
    # Step 2: Show activation instructions
    print("\nVirtual environment activation:")
    activate_virtual_env("venv")
    
    # Step 3: Install requirements
    print("\nInstalling requirements...")
    install_requirements()
    
    print("\nSetup completed successfully!")
    print("Don't forget to activate your virtual environment before working.")

if __name__ == "__main__":
    main()