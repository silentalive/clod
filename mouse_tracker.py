#!/usr/bin/env python3
"""
Mouse Movement Tracker
Tracks mouse movements across the screen and visualizes pixel coverage.
"""

import numpy as np
import time
import json
from datetime import datetime
from pathlib import Path
from pynput import mouse
from PIL import Image, ImageDraw
import threading
import sys


class MouseTracker:
    def __init__(self, screen_width=1920, screen_height=1080):
        """
        Initialize the mouse tracker.

        Args:
            screen_width: Width of the screen in pixels
            screen_height: Height of the screen in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.heatmap = np.zeros((screen_height, screen_width), dtype=np.uint32)
        self.is_tracking = False
        self.listener = None
        self.start_time = None
        self.total_movements = 0

    def on_move(self, x, y):
        """Callback function for mouse movement."""
        if self.is_tracking:
            # Ensure coordinates are within bounds
            x = max(0, min(x, self.screen_width - 1))
            y = max(0, min(y, self.screen_height - 1))

            self.heatmap[y, x] += 1
            self.total_movements += 1

            # Print progress every 1000 movements
            if self.total_movements % 1000 == 0:
                print(f"Tracked {self.total_movements:,} movements...", end='\r')

    def start(self):
        """Start tracking mouse movements."""
        if self.is_tracking:
            print("Tracking is already running!")
            return

        print(f"Starting mouse tracking on {self.screen_width}x{self.screen_height} screen...")
        print("Press Ctrl+C to stop tracking and generate visualization.")

        self.is_tracking = True
        self.start_time = datetime.now()

        # Start the mouse listener in a separate thread
        self.listener = mouse.Listener(on_move=self.on_move)
        self.listener.start()

    def stop(self):
        """Stop tracking mouse movements."""
        if not self.is_tracking:
            print("Tracking is not running!")
            return

        print("\nStopping mouse tracking...")
        self.is_tracking = False

        if self.listener:
            self.listener.stop()
            self.listener.join()

        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        print(f"Tracking session completed:")
        print(f"  Duration: {elapsed_time:.1f} seconds")
        print(f"  Total movements: {self.total_movements:,}")
        print(f"  Unique pixels visited: {np.count_nonzero(self.heatmap):,}")

    def save_data(self, filename="mouse_data.npz"):
        """Save the heatmap data to a file."""
        np.savez_compressed(
            filename,
            heatmap=self.heatmap,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            total_movements=self.total_movements,
            timestamp=datetime.now().isoformat()
        )
        print(f"Data saved to {filename}")

    def load_data(self, filename="mouse_data.npz"):
        """Load heatmap data from a file."""
        data = np.load(filename)
        self.heatmap = data['heatmap']
        self.screen_width = int(data['screen_width'])
        self.screen_height = int(data['screen_height'])
        self.total_movements = int(data['total_movements'])
        print(f"Data loaded from {filename}")

    def generate_heatmap(self, output_file="mouse_heatmap.png", scale=0.5):
        """
        Generate a heatmap visualization.

        Args:
            output_file: Path to save the heatmap image
            scale: Scale factor for the output image (0.5 = half size)
        """
        print("Generating heatmap visualization...")

        # Normalize the heatmap to 0-255 range for visualization
        if self.heatmap.max() > 0:
            normalized = np.log1p(self.heatmap)  # Log scale for better visualization
            normalized = (normalized / normalized.max() * 255).astype(np.uint8)
        else:
            normalized = np.zeros_like(self.heatmap, dtype=np.uint8)

        # Create a colored heatmap using a custom color gradient
        # Blue (cold) -> Green -> Yellow -> Red (hot)
        colored = np.zeros((self.screen_height, self.screen_width, 3), dtype=np.uint8)

        # Apply color gradient
        for i in range(self.screen_height):
            for j in range(self.screen_width):
                value = normalized[i, j]
                if value == 0:
                    # Black for unvisited pixels
                    colored[i, j] = [0, 0, 0]
                elif value < 64:
                    # Blue
                    colored[i, j] = [0, 0, value * 4]
                elif value < 128:
                    # Blue to Green
                    t = (value - 64) / 64
                    colored[i, j] = [0, int(255 * t), int(255 * (1 - t))]
                elif value < 192:
                    # Green to Yellow
                    t = (value - 128) / 64
                    colored[i, j] = [int(255 * t), 255, 0]
                else:
                    # Yellow to Red
                    t = (value - 192) / 63
                    colored[i, j] = [255, int(255 * (1 - t)), 0]

        # Create PIL image
        img = Image.fromarray(colored, 'RGB')

        # Scale down if requested
        if scale != 1.0:
            new_size = (int(self.screen_width * scale), int(self.screen_height * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        # Save the image
        img.save(output_file)
        print(f"Heatmap saved to {output_file}")

    def get_statistics(self):
        """Get detailed statistics about mouse movements."""
        stats = {
            'total_movements': self.total_movements,
            'unique_pixels': int(np.count_nonzero(self.heatmap)),
            'max_visits': int(self.heatmap.max()),
            'screen_coverage': f"{(np.count_nonzero(self.heatmap) / (self.screen_width * self.screen_height) * 100):.2f}%",
            'screen_size': f"{self.screen_width}x{self.screen_height}"
        }

        if self.heatmap.max() > 0:
            max_pos = np.unravel_index(self.heatmap.argmax(), self.heatmap.shape)
            stats['most_visited_pixel'] = f"({max_pos[1]}, {max_pos[0]})"

        return stats

    def print_statistics(self):
        """Print detailed statistics."""
        stats = self.get_statistics()
        print("\n" + "=" * 50)
        print("MOUSE TRACKING STATISTICS")
        print("=" * 50)
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        print("=" * 50)


def detect_screen_size():
    """Attempt to detect the screen size."""
    try:
        from screeninfo import get_monitors
        monitors = get_monitors()
        if monitors:
            primary = monitors[0]
            return primary.width, primary.height
    except ImportError:
        pass

    # Default fallback
    return 1920, 1080


def main():
    """Main function to run the mouse tracker."""
    print("=" * 60)
    print("MOUSE MOVEMENT TRACKER")
    print("=" * 60)

    # Try to detect screen size
    width, height = detect_screen_size()
    print(f"Detected screen size: {width}x{height}")
    print("(If incorrect, modify the values in the script)")
    print()

    tracker = MouseTracker(screen_width=width, screen_height=height)

    try:
        tracker.start()

        # Keep the program running until interrupted
        while tracker.is_tracking:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user...")
    finally:
        tracker.stop()
        tracker.print_statistics()

        # Save data and generate visualizations
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data_file = f"mouse_data_{timestamp}.npz"
        heatmap_file = f"mouse_heatmap_{timestamp}.png"

        tracker.save_data(data_file)
        tracker.generate_heatmap(heatmap_file, scale=0.5)

        print("\nAll done! Check the generated files:")
        print(f"  - {data_file} (raw data)")
        print(f"  - {heatmap_file} (visualization)")


if __name__ == "__main__":
    main()
