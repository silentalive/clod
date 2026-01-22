# 🖱️ Mouse Movement Tracker

A beautiful Python application that tracks and visualizes your mouse movements across the screen. See exactly how often your cursor has passed over each pixel with stunning heatmap visualizations.

## 📥 Download (Kein Python benötigt!)

**Fertiges Programm direkt herunterladen:**

👉 **[Zur Download-Seite (Releases)](../../releases/latest)**

Einfach die Version für dein Betriebssystem herunterladen und starten:
- 🪟 **Windows**: `MouseTracker-Windows.exe` (Doppelklick zum Starten)
- 🐧 **Linux**: `MouseTracker-Linux` (Ausführbar machen: `chmod +x`, dann starten)
- 🍎 **macOS**: `MouseTracker-macOS` (Rechtsklick → Öffnen beim ersten Start)

**Keine Installation nötig** - einfach runterladen und loslegen! 🚀

---

**Oder als Python-Script ausführen:**

**Available in two versions:**
- 🎨 **GUI Version** - Modern, minimalistic interface (recommended)
- ⌨️ **CLI Version** - Command-line interface for advanced users

## ✨ Features

### GUI Version (mouse_tracker_gui.py)
- 🎨 Modern, rounded design with dark theme
- ⚙️ Easy settings panel for screen size configuration
- 📊 Real-time statistics display
- 🎯 Live tracking status and progress
- 💾 Save and load sessions with file dialogs
- 🖼️ Built-in heatmap preview window
- 📤 Export heatmaps to full resolution
- 🚀 Can be built as standalone executable

### CLI Version (mouse_tracker.py)
- Real-time mouse movement tracking
- Pixel-level precision tracking
- Automatic screen size detection
- Beautiful heatmap visualization with color gradients
- Detailed statistics about your mouse usage
- Save and load tracking sessions
- Low memory footprint using NumPy

## 🚀 Quick Start

### Easiest Way (Recommended)

**Windows:**
1. Double-click `run_gui.bat`

**Linux/Mac:**
1. Make executable: `chmod +x run_gui.sh`
2. Run: `./run_gui.sh`

**Or manually:**
```bash
python run_gui.py
```

The launcher will automatically install missing dependencies and start the GUI!

### Manual Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the GUI version:
```bash
python mouse_tracker_gui.py
```

## 📖 Usage Guide

### GUI Version (Recommended)

Start the GUI application:

```bash
python mouse_tracker_gui.py
```

**Interface Overview:**
- **Settings Panel**: Configure your screen width and height
- **Start/Stop Button**: Begin or end tracking
- **Live Statistics**: See real-time tracking data
  - Duration: How long you've been tracking
  - Movements: Total mouse movements recorded
  - Unique Pixels: How many different pixels were visited
  - Coverage: Percentage of screen covered
  - Max Visits: Highest number of visits to a single pixel
- **Save/Load**: Save your session or load previous data
- **Preview**: Generate and view heatmap visualization

**Workflow:**
1. Adjust screen size in settings if needed (auto-detected by default)
2. Click "▶ Start Tracking"
3. Move your mouse around
4. Click "⏸ Stop Tracking" when done
5. Click "🎨 Generate Heatmap Preview" to see visualization
6. Export full resolution or save data for later

### CLI Version

Run the command-line tracker:

```bash
python mouse_tracker.py
```

The tracker will:
1. Automatically detect your screen size
2. Start tracking mouse movements
3. Show real-time progress every 1000 movements
4. Wait for you to press `Ctrl+C` to stop

When you stop tracking (press `Ctrl+C`), it will automatically:
- Display detailed statistics
- Save the raw data to a `.npz` file
- Generate a heatmap visualization as a `.png` image

### Output Files

The tracker generates two files with timestamps:

- `mouse_data_YYYYMMDD_HHMMSS.npz` - Raw tracking data (can be reloaded)
- `mouse_heatmap_YYYYMMDD_HHMMSS.png` - Heatmap visualization

### Understanding the Heatmap

The heatmap uses a color gradient to show mouse activity:

- **Black**: Never visited
- **Blue**: Low activity (few passes)
- **Green**: Moderate activity
- **Yellow**: High activity
- **Red**: Very high activity (most visited pixels)

The heatmap uses logarithmic scaling for better visualization of varying activity levels.

## Statistics

The tracker provides detailed statistics including:

- Total number of mouse movements recorded
- Number of unique pixels visited
- Screen coverage percentage
- Most visited pixel location
- Maximum number of visits to any single pixel

## Example Session

```
==============================================================
MOUSE MOVEMENT TRACKER
==============================================================
Detected screen size: 1920x1080
(If incorrect, modify the values in the script)

Starting mouse tracking on 1920x1080 screen...
Press Ctrl+C to stop tracking and generate visualization.
Tracked 15,000 movements...
^C
Interrupted by user...

Stopping mouse tracking...
Tracking session completed:
  Duration: 180.5 seconds
  Total movements: 15,234
  Unique pixels visited: 12,450

==================================================
MOUSE TRACKING STATISTICS
==================================================
Total Movements: 15234
Unique Pixels: 12450
Max Visits: 156
Screen Coverage: 0.60%
Screen Size: 1920x1080
Most Visited Pixel: (960, 540)
==================================================

Data saved to mouse_data_20260122_143025.npz
Generating heatmap visualization...
Heatmap saved to mouse_heatmap_20260122_143025.png

All done! Check the generated files:
  - mouse_data_20260122_143025.npz (raw data)
  - mouse_heatmap_20260122_143025.png (visualization)
```

## Customization

### Screen Size

If automatic detection doesn't work, manually set your screen size in the script:

```python
tracker = MouseTracker(screen_width=1920, screen_height=1080)
```

### Heatmap Scale

Change the output image scale (default is 0.5 for half resolution):

```python
tracker.generate_heatmap("output.png", scale=0.5)  # 50% of original size
tracker.generate_heatmap("output.png", scale=1.0)  # Full resolution
```

## Advanced Usage

### Loading Previous Sessions

You can load and visualize previously saved tracking data:

```python
from mouse_tracker import MouseTracker

tracker = MouseTracker()
tracker.load_data("mouse_data_20260122_143025.npz")
tracker.print_statistics()
tracker.generate_heatmap("new_visualization.png")
```

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.7+
- **RAM**: Minimal (approximately 8-16 MB for 1920x1080 screen)
- **Permissions**: May require accessibility permissions on macOS

### macOS Permissions

On macOS, you may need to grant accessibility permissions:
1. Go to System Preferences → Security & Privacy → Privacy → Accessibility
2. Add your terminal application or Python to the allowed list

## Troubleshooting

### ImportError: No module named 'pynput'

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Screen size detection not working

Manually specify your screen size in the `main()` function:
```python
tracker = MouseTracker(screen_width=YOUR_WIDTH, screen_height=YOUR_HEIGHT)
```

### Permission denied on Linux/macOS

You may need to run with appropriate permissions for mouse event capture:
```bash
sudo python mouse_tracker.py  # Use with caution
```

## 📚 Dependencies

- **numpy**: Efficient array operations for pixel tracking
- **Pillow**: Image generation and manipulation
- **pynput**: Cross-platform mouse event listener
- **screeninfo**: Screen size detection (optional)
- **customtkinter**: Modern GUI framework (for GUI version only)

## Performance

- Very low CPU usage (event-driven)
- Memory usage scales with screen resolution:
  - 1920x1080: ~8 MB
  - 2560x1440: ~14 MB
  - 3840x2160: ~32 MB

## Use Cases

- Analyze your mouse movement patterns
- Identify frequently used screen areas
- Optimize UI/UX by understanding user behavior
- Create unique data visualizations
- Ergonomics studies
- Productivity analysis

## License

This project is provided as-is for educational and personal use.

## 📦 Building Standalone Executable

Want to create a standalone program that doesn't require Python?

### Build Instructions

1. Install PyInstaller (if not already installed):
```bash
pip install pyinstaller
```

2. Run the build script:
```bash
python build_executable.py
```

3. Find your executable in the `dist/` folder:
   - **Windows**: `dist/MouseTracker.exe`
   - **Linux/Mac**: `dist/MouseTracker`

4. Double-click to run - no Python installation needed!

**Note**: The executable will be 50-100 MB due to bundled dependencies.

## 📁 Project Files

- `mouse_tracker_gui.py` - Modern GUI application
- `mouse_tracker.py` - CLI version
- `example_analysis.py` - Script for analyzing saved data
- `run_gui.py` - Smart launcher with dependency checking
- `run_gui.bat` / `run_gui.sh` - Platform-specific launchers
- `build_executable.py` - Build standalone executable
- `requirements.txt` - Python dependencies

## 🎨 GUI Screenshots

The GUI features:
- Clean, modern dark theme
- Rounded corners and smooth design
- Real-time statistics cards
- Interactive buttons with hover effects
- File dialogs for save/load
- Popup preview window for heatmaps

## 🔧 For Developers

### Creating a New Release

Releases are automatically built by GitHub Actions. To create a new release:

**Option 1: Use the helper script**
```bash
# Linux/Mac
./create_release.sh

# Windows
create_release.bat
```

**Option 2: Manual**
```bash
# Create and push a version tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

GitHub Actions will automatically:
1. Build executables for Windows, Linux, and macOS
2. Create a GitHub Release
3. Upload all executables as downloadable assets

### CI/CD Workflows

This project includes two GitHub Actions workflows:

- **`build-executables.yml`**: Triggered on version tags (v*), builds and publishes releases
- **`test-build.yml`**: Triggered on pushes/PRs, tests builds on all platforms

## Contributing

Feel free to fork and improve this project. Suggestions for improvements:

- ✅ ~~Real-time visualization window~~ (Implemented in GUI)
- ✅ ~~Settings panel~~ (Implemented in GUI)
- ✅ ~~Automated builds~~ (Implemented with GitHub Actions)
- Multiple monitor support
- Click tracking alongside movement
- Path replay functionality
- Export to different image formats
- Custom color schemes
- Hotkey support for starting/stopping

## Privacy Note

All tracking data is stored locally on your computer. No data is transmitted or shared externally.
