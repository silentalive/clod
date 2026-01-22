#!/usr/bin/env python3
"""
Example script showing how to load and analyze saved mouse tracking data.
"""

from mouse_tracker import MouseTracker
import sys


def analyze_session(data_file):
    """
    Load and analyze a previously saved mouse tracking session.

    Args:
        data_file: Path to the .npz data file
    """
    print(f"Loading data from {data_file}...")

    tracker = MouseTracker()
    tracker.load_data(data_file)

    # Print statistics
    tracker.print_statistics()

    # Generate different visualizations
    print("\nGenerating visualizations...")

    # Full resolution heatmap
    tracker.generate_heatmap("heatmap_full.png", scale=1.0)

    # Half resolution (smaller file)
    tracker.generate_heatmap("heatmap_half.png", scale=0.5)

    # Quarter resolution (for quick preview)
    tracker.generate_heatmap("heatmap_preview.png", scale=0.25)

    print("\nAnalysis complete!")
    print("Generated files:")
    print("  - heatmap_full.png (full resolution)")
    print("  - heatmap_half.png (50% scale)")
    print("  - heatmap_preview.png (25% scale)")

    # Get statistics as dictionary for further processing
    stats = tracker.get_statistics()

    # Example: Calculate average visits per visited pixel
    if stats['unique_pixels'] > 0:
        avg_visits = stats['total_movements'] / stats['unique_pixels']
        print(f"\nAverage visits per visited pixel: {avg_visits:.2f}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python example_analysis.py <mouse_data_file.npz>")
        print("\nExample:")
        print("  python example_analysis.py mouse_data_20260122_143025.npz")
        sys.exit(1)

    data_file = sys.argv[1]
    analyze_session(data_file)
