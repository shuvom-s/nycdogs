#!/usr/bin/env python3
"""
Local setup helper for NYC Dogs Map project.
This script helps set up your local environment for running the Flask app.
"""

import sys
import subprocess
import os

def check_python_version():
    """Check if Python version is compatible"""
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print(f"Warning: You're using Python {python_version.major}.{python_version.minor}.")
        print("This project works best with Python 3.8 or newer.")
        return False
    return True

def install_dependencies():
    """Install the required dependencies with specific versions"""
    print("Installing dependencies...")
    try:
        # Install specific versions that we know work together
        subprocess.check_call([sys.executable, "-m", "pip", "install", 
                               "Flask==2.2.3", 
                               "Werkzeug==2.2.3"])
        
        # Install other requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def check_data_files():
    """Check if required data files exist"""
    required_files = ['nycdogs.csv', 'ZCTA.gpkg']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print("Warning: The following required files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        print("\nPlease ensure these files are in the project root directory.")
        return False
    return True

def main():
    """Run the setup process"""
    print("="*60)
    print("NYC Dogs Map - Local Setup Helper")
    print("="*60)
    
    # Check Python version
    python_ok = check_python_version()
    
    # Install dependencies
    deps_ok = install_dependencies()
    
    # Check data files
    data_ok = check_data_files()
    
    # Summary
    print("\n" + "="*60)
    if python_ok and deps_ok and data_ok:
        print("Setup completed successfully!")
        print("\nYou can now run the Flask app with:")
        print("  python app.py")
    else:
        print("Setup completed with warnings.")
        print("Please address the issues mentioned above before running the app.")
    
    print("="*60)

if __name__ == "__main__":
    main() 