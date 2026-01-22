# Mouse Movement Tracker

A Python application that tracks and visualizes your mouse movements across the screen. See exactly how often your cursor has passed over each pixel with beautiful heatmap visualizations.

## Features

- Real-time mouse movement tracking
- Pixel-level precision tracking
- Automatic screen size detection
- Beautiful heatmap visualization with color gradients
- Detailed statistics about your mouse usage
- Save and load tracking sessions
- Low memory footprint using NumPy

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Simply run the tracker:

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

## Dependencies

- **numpy**: Efficient array operations for pixel tracking
- **Pillow**: Image generation and manipulation
- **pynput**: Cross-platform mouse event listener
- **screeninfo**: Screen size detection (optional)

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

## Contributing

Feel free to fork and improve this project. Suggestions for improvements:

- Real-time visualization window
- Multiple monitor support
- Click tracking alongside movement
- Path replay functionality
- Export to different image formats
- Custom color schemes

## Privacy Note

All tracking data is stored locally on your computer. No data is transmitted or shared externally.
