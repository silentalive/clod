#!/usr/bin/env python3
"""
Simple launcher for the Mouse Tracker GUI.
Double-click this file to start the application!
"""

import sys
import subprocess
from pathlib import Path


def check_dependencies():
    """Check if all dependencies are installed."""
    missing = []

    try:
        import customtkinter
    except ImportError:
        missing.append("customtkinter")

    try:
        import numpy
    except ImportError:
        missing.append("numpy")

    try:
        import PIL
    except ImportError:
        missing.append("Pillow")

    try:
        import pynput
    except ImportError:
        missing.append("pynput")

    return missing


def install_dependencies(missing):
    """Install missing dependencies."""
    print("Installing missing dependencies...")
    print(f"Missing: {', '.join(missing)}")
    print()

    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print()
        print("✓ Dependencies installed successfully!")
        print()
        return True
    except subprocess.CalledProcessError:
        print()
        print("✗ Failed to install dependencies!")
        print("Please run manually: pip install -r requirements.txt")
        return False


def main():
    """Main launcher."""
    print("=" * 60)
    print("Mouse Movement Tracker - GUI Launcher")
    print("=" * 60)
    print()

    # Check dependencies
    missing = check_dependencies()

    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print()
        response = input("Install missing dependencies? (y/n): ").lower()

        if response == 'y':
            if not install_dependencies(missing):
                input("Press Enter to exit...")
                sys.exit(1)
        else:
            print("Cannot start without dependencies.")
            input("Press Enter to exit...")
            sys.exit(1)
    else:
        print("✓ All dependencies are installed")
        print()

    # Start the GUI
    print("Starting Mouse Tracker GUI...")
    print()

    try:
        from mouse_tracker_gui import main as gui_main
        gui_main()
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ Error starting GUI!")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        import traceback
        traceback.print_exc()
        print()
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
