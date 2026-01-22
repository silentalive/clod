#!/usr/bin/env python3
"""
Build script to create standalone executable for Mouse Tracker GUI.
"""

import subprocess
import sys
import os
from pathlib import Path


def build_executable():
    """Build the standalone executable using PyInstaller."""

    print("=" * 60)
    print("Mouse Tracker - Executable Builder")
    print("=" * 60)
    print()

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")

    print()
    print("Building executable...")
    print("This may take a few minutes...")
    print()

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=MouseTracker",
        "--onefile",
        "--windowed",
        "--icon=NONE",
        "--add-data=README.md:.",
        "mouse_tracker_gui.py"
    ]

    try:
        subprocess.check_call(cmd)
        print()
        print("=" * 60)
        print("✓ Build successful!")
        print("=" * 60)
        print()
        print("Executable location:")

        if sys.platform == "win32":
            exe_path = Path("dist") / "MouseTracker.exe"
            print(f"  {exe_path.absolute()}")
            print()
            print("You can now double-click MouseTracker.exe to run the program!")
        else:
            exe_path = Path("dist") / "MouseTracker"
            print(f"  {exe_path.absolute()}")
            print()
            print("Run with: ./dist/MouseTracker")

    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print("✗ Build failed!")
        print("=" * 60)
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_executable()
