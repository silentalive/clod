#!/usr/bin/env python3
"""
Mouse Movement Tracker - GUI Version
Modern, minimalistic interface for tracking and visualizing mouse movements.
"""

import customtkinter as ctk
import numpy as np
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from pynput import mouse
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox


class MouseTrackerGUI:
    def __init__(self):
        # Set appearance and theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Main window
        self.root = ctk.CTk()
        self.root.title("Mouse Movement Tracker")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        # Tracking state
        self.is_tracking = False
        self.listener = None
        self.heatmap = None
        self.start_time = None
        self.total_movements = 0
        self.screen_width = 1920
        self.screen_height = 1080

        # UI update
        self.update_interval = 500  # ms
        self.last_update = time.time()

        self.setup_ui()
        self.detect_screen_size()

    def setup_ui(self):
        """Setup the user interface."""
        # Main container with padding
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="🖱️ Mouse Movement Tracker",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(0, 20))

        # Top section: Controls and Settings
        top_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        top_frame.pack(fill="x", pady=(0, 15))

        self.setup_controls(top_frame)

        # Middle section: Settings
        settings_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        settings_frame.pack(fill="x", pady=(0, 15))

        self.setup_settings(settings_frame)

        # Bottom section: Statistics and Preview
        bottom_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        bottom_frame.pack(fill="both", expand=True)

        self.setup_statistics(bottom_frame)

    def setup_controls(self, parent):
        """Setup control buttons."""
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)

        # Status indicator
        self.status_frame = ctk.CTkFrame(parent, corner_radius=10)
        self.status_frame.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 10), sticky="ew")

        self.status_indicator = ctk.CTkLabel(
            self.status_frame,
            text="⚫",
            font=ctk.CTkFont(size=20)
        )
        self.status_indicator.pack(side="left", padx=(10, 5))

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready to track",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.status_label.pack(side="left", padx=5)

        # Start/Stop button
        self.start_button = ctk.CTkButton(
            parent,
            text="▶ Start Tracking",
            command=self.toggle_tracking,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.start_button.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Save button
        self.save_button = ctk.CTkButton(
            parent,
            text="💾 Save Data",
            command=self.save_data,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            state="disabled"
        )
        self.save_button.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="ew")

        # Load button
        load_button = ctk.CTkButton(
            parent,
            text="📁 Load Data",
            command=self.load_data,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10
        )
        load_button.grid(row=1, column=2, padx=20, pady=(0, 20), sticky="ew")

    def setup_settings(self, parent):
        """Setup settings panel."""
        settings_label = ctk.CTkLabel(
            parent,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        settings_label.pack(pady=(15, 10), padx=20, anchor="w")

        # Settings grid
        settings_grid = ctk.CTkFrame(parent, fg_color="transparent")
        settings_grid.pack(fill="x", padx=20, pady=(0, 15))

        settings_grid.grid_columnconfigure(1, weight=1)

        # Screen width
        ctk.CTkLabel(
            settings_grid,
            text="Screen Width:",
            font=ctk.CTkFont(size=14)
        ).grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")

        self.width_entry = ctk.CTkEntry(
            settings_grid,
            placeholder_text="1920",
            height=35,
            corner_radius=8
        )
        self.width_entry.grid(row=0, column=1, pady=5, sticky="ew")
        self.width_entry.insert(0, str(self.screen_width))

        # Screen height
        ctk.CTkLabel(
            settings_grid,
            text="Screen Height:",
            font=ctk.CTkFont(size=14)
        ).grid(row=1, column=0, padx=(0, 10), pady=5, sticky="w")

        self.height_entry = ctk.CTkEntry(
            settings_grid,
            placeholder_text="1080",
            height=35,
            corner_radius=8
        )
        self.height_entry.grid(row=1, column=1, pady=5, sticky="ew")
        self.height_entry.insert(0, str(self.screen_height))

        # Apply button
        apply_button = ctk.CTkButton(
            settings_grid,
            text="✓ Apply Settings",
            command=self.apply_settings,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=13)
        )
        apply_button.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="ew")

    def setup_statistics(self, parent):
        """Setup statistics display."""
        stats_label = ctk.CTkLabel(
            parent,
            text="📊 Statistics",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        stats_label.pack(pady=(15, 10), padx=20, anchor="w")

        # Statistics grid
        stats_grid = ctk.CTkFrame(parent, fg_color="transparent")
        stats_grid.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        stats_grid.grid_columnconfigure((0, 1, 2), weight=1)

        # Tracking duration
        self.duration_card = self.create_stat_card(
            stats_grid, "⏱️ Duration", "0:00:00", 0, 0
        )

        # Total movements
        self.movements_card = self.create_stat_card(
            stats_grid, "🔢 Movements", "0", 0, 1
        )

        # Unique pixels
        self.pixels_card = self.create_stat_card(
            stats_grid, "🎯 Unique Pixels", "0", 0, 2
        )

        # Screen coverage
        self.coverage_card = self.create_stat_card(
            stats_grid, "📍 Coverage", "0.00%", 1, 0
        )

        # Max visits
        self.max_visits_card = self.create_stat_card(
            stats_grid, "🔥 Max Visits", "0", 1, 1
        )

        # Screen size
        self.screen_size_card = self.create_stat_card(
            stats_grid, "🖥️ Screen Size", f"{self.screen_width}x{self.screen_height}", 1, 2
        )

        # Preview button
        self.preview_button = ctk.CTkButton(
            parent,
            text="🎨 Generate Heatmap Preview",
            command=self.show_heatmap_preview,
            height=40,
            font=ctk.CTkFont(size=15, weight="bold"),
            corner_radius=10,
            state="disabled"
        )
        self.preview_button.pack(pady=(10, 15), padx=20, fill="x")

    def create_stat_card(self, parent, title, value, row, col):
        """Create a statistic card."""
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        title_label.pack(pady=(15, 5))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=22, weight="bold")
        )
        value_label.pack(pady=(0, 15))

        return value_label

    def detect_screen_size(self):
        """Detect screen size automatically."""
        try:
            from screeninfo import get_monitors
            monitors = get_monitors()
            if monitors:
                primary = monitors[0]
                self.screen_width = primary.width
                self.screen_height = primary.height
                self.width_entry.delete(0, tk.END)
                self.width_entry.insert(0, str(self.screen_width))
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(0, str(self.screen_height))
                self.update_screen_size_display()
        except:
            pass

    def apply_settings(self):
        """Apply screen size settings."""
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())

            if width < 100 or height < 100 or width > 10000 or height > 10000:
                messagebox.showerror("Error", "Invalid screen size! Use values between 100 and 10000.")
                return

            self.screen_width = width
            self.screen_height = height

            # Reset heatmap with new size
            if not self.is_tracking:
                self.heatmap = np.zeros((height, width), dtype=np.uint32)
                self.total_movements = 0

            self.update_screen_size_display()
            messagebox.showinfo("Success", f"Screen size set to {width}x{height}")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

    def update_screen_size_display(self):
        """Update screen size display in statistics."""
        self.screen_size_card.configure(text=f"{self.screen_width}x{self.screen_height}")

    def toggle_tracking(self):
        """Toggle mouse tracking on/off."""
        if self.is_tracking:
            self.stop_tracking()
        else:
            self.start_tracking()

    def start_tracking(self):
        """Start tracking mouse movements."""
        self.is_tracking = True
        self.start_time = datetime.now()
        self.heatmap = np.zeros((self.screen_height, self.screen_width), dtype=np.uint32)
        self.total_movements = 0

        # Update UI
        self.start_button.configure(
            text="⏸ Stop Tracking",
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        self.status_indicator.configure(text="🔴")
        self.status_label.configure(text="Tracking active...")
        self.save_button.configure(state="disabled")
        self.preview_button.configure(state="disabled")

        # Start listener
        self.listener = mouse.Listener(on_move=self.on_move)
        self.listener.start()

        # Start UI update loop
        self.update_statistics()

    def stop_tracking(self):
        """Stop tracking mouse movements."""
        self.is_tracking = False

        if self.listener:
            self.listener.stop()
            self.listener.join()

        # Update UI
        self.start_button.configure(
            text="▶ Start Tracking",
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.status_indicator.configure(text="🟢")
        self.status_label.configure(text="Tracking stopped")
        self.save_button.configure(state="normal")

        if self.total_movements > 0:
            self.preview_button.configure(state="normal")

    def on_move(self, x, y):
        """Callback for mouse movement."""
        if self.is_tracking:
            # Ensure coordinates are within bounds
            x = max(0, min(x, self.screen_width - 1))
            y = max(0, min(y, self.screen_height - 1))

            self.heatmap[y, x] += 1
            self.total_movements += 1

    def update_statistics(self):
        """Update statistics display."""
        if not self.is_tracking and self.start_time is None:
            return

        # Duration
        if self.start_time:
            duration = datetime.now() - self.start_time
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            seconds = int(duration.total_seconds() % 60)
            self.duration_card.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

        # Movements
        self.movements_card.configure(text=f"{self.total_movements:,}")

        # Unique pixels
        if self.heatmap is not None:
            unique_pixels = np.count_nonzero(self.heatmap)
            self.pixels_card.configure(text=f"{unique_pixels:,}")

            # Coverage
            total_pixels = self.screen_width * self.screen_height
            coverage = (unique_pixels / total_pixels * 100) if total_pixels > 0 else 0
            self.coverage_card.configure(text=f"{coverage:.2f}%")

            # Max visits
            max_visits = int(self.heatmap.max())
            self.max_visits_card.configure(text=f"{max_visits:,}")

        # Schedule next update
        if self.is_tracking:
            self.root.after(self.update_interval, self.update_statistics)

    def save_data(self):
        """Save tracking data to file."""
        if self.heatmap is None or self.total_movements == 0:
            messagebox.showwarning("Warning", "No data to save!")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"mouse_data_{timestamp}"

        filename = filedialog.asksaveasfilename(
            defaultextension=".npz",
            initialfile=default_name,
            filetypes=[("NumPy Archive", "*.npz"), ("All Files", "*.*")]
        )

        if filename:
            np.savez_compressed(
                filename,
                heatmap=self.heatmap,
                screen_width=self.screen_width,
                screen_height=self.screen_height,
                total_movements=self.total_movements,
                timestamp=datetime.now().isoformat()
            )
            messagebox.showinfo("Success", f"Data saved to:\n{filename}")

    def load_data(self):
        """Load tracking data from file."""
        filename = filedialog.askopenfilename(
            filetypes=[("NumPy Archive", "*.npz"), ("All Files", "*.*")]
        )

        if filename:
            try:
                data = np.load(filename)
                self.heatmap = data['heatmap']
                self.screen_width = int(data['screen_width'])
                self.screen_height = int(data['screen_height'])
                self.total_movements = int(data['total_movements'])

                # Update UI
                self.width_entry.delete(0, tk.END)
                self.width_entry.insert(0, str(self.screen_width))
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(0, str(self.screen_height))

                self.start_time = datetime.now()  # Reset start time
                self.update_screen_size_display()
                self.update_statistics()

                self.preview_button.configure(state="normal")
                self.save_button.configure(state="normal")

                messagebox.showinfo("Success", f"Data loaded from:\n{filename}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data:\n{str(e)}")

    def show_heatmap_preview(self):
        """Show heatmap preview in new window."""
        if self.heatmap is None or self.total_movements == 0:
            messagebox.showwarning("Warning", "No data to visualize!")
            return

        # Create preview window
        preview = ctk.CTkToplevel(self.root)
        preview.title("Heatmap Preview")
        preview.geometry("800x650")

        # Title
        title = ctk.CTkLabel(
            preview,
            text="🎨 Heatmap Visualization",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)

        # Generate heatmap image
        heatmap_img = self.generate_heatmap_image(max_width=750, max_height=500)

        # Display image
        img_label = ctk.CTkLabel(preview, text="", image=heatmap_img)
        img_label.image = heatmap_img  # Keep reference
        img_label.pack(pady=10)

        # Export button
        def export_full():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                initialfile=f"mouse_heatmap_{timestamp}",
                filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")]
            )
            if filename:
                full_img = self.generate_heatmap_pil()
                full_img.save(filename)
                messagebox.showinfo("Success", f"Heatmap saved to:\n{filename}")

        export_btn = ctk.CTkButton(
            preview,
            text="💾 Export Full Resolution",
            command=export_full,
            height=40,
            font=ctk.CTkFont(size=15, weight="bold"),
            corner_radius=10
        )
        export_btn.pack(pady=10)

    def generate_heatmap_pil(self):
        """Generate PIL heatmap image."""
        # Normalize the heatmap
        if self.heatmap.max() > 0:
            normalized = np.log1p(self.heatmap)
            normalized = (normalized / normalized.max() * 255).astype(np.uint8)
        else:
            normalized = np.zeros_like(self.heatmap, dtype=np.uint8)

        # Create colored heatmap
        colored = np.zeros((self.screen_height, self.screen_width, 3), dtype=np.uint8)

        for i in range(self.screen_height):
            for j in range(self.screen_width):
                value = normalized[i, j]
                if value == 0:
                    colored[i, j] = [0, 0, 0]
                elif value < 64:
                    colored[i, j] = [0, 0, value * 4]
                elif value < 128:
                    t = (value - 64) / 64
                    colored[i, j] = [0, int(255 * t), int(255 * (1 - t))]
                elif value < 192:
                    t = (value - 128) / 64
                    colored[i, j] = [int(255 * t), 255, 0]
                else:
                    t = (value - 192) / 63
                    colored[i, j] = [255, int(255 * (1 - t)), 0]

        return Image.fromarray(colored, 'RGB')

    def generate_heatmap_image(self, max_width=750, max_height=500):
        """Generate heatmap image for preview."""
        img = self.generate_heatmap_pil()

        # Calculate scaling to fit in preview
        scale_w = max_width / self.screen_width
        scale_h = max_height / self.screen_height
        scale = min(scale_w, scale_h, 1.0)

        new_size = (int(self.screen_width * scale), int(self.screen_height * scale))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

        return ImageTk.PhotoImage(img)

    def run(self):
        """Run the application."""
        self.root.mainloop()


def main():
    """Main entry point."""
    app = MouseTrackerGUI()
    app.run()


if __name__ == "__main__":
    main()
