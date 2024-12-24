import pygame
import math  # Move this import outside the class definition
import random

class Driver:
    def __init__(self, name, color, speed=0.01):
        self.name = name
        self.color = color
        self.speed = speed  # Base speed
        self.progress = 0.0  # Progress on track
        self.lap = 1  # Start from lap 1
        self.time_gap = 0.0  # Time gap behind the leader

    def update_progress(self, delta_time, track_length, boost=1.0):
        """Update the driver's progress."""
        self.progress += (self.speed * boost * delta_time) / track_length
        if self.progress >= 1.0:  # Complete a lap
            self.progress -= 1.0
            self.lap += 1

def generate_boot_track(screen_width, screen_height):
    """Generate waypoints for a boot-shaped track."""
    track = [
        (100, 300), (150, 250), (200, 200), (300, 150), (400, 100),  # Boot top
        (500, 150), (550, 200), (500, 300), (450, 350),              # Boot heel curve
        (350, 450), (250, 500), (150, 450), (100, 400),             # Boot sole
        (100, 300)  # Closing loop
    ]
    return scale_track(track, screen_width, screen_height)

def scale_track(track, screen_width, screen_height, margin=50):
    """
    Scale the track coordinates to fit within the screen dimensions.
    :param track: List of (x, y) waypoints.
    :param screen_width: Width of the screen.
    :param screen_height: Height of the screen.
    :param margin: Margin to leave around the track.
    :return: Scaled list of (x, y) waypoints.
    """
    # Find the min and max values of the original track
    min_x = min(point[0] for point in track)
    max_x = max(point[0] for point in track)
    min_y = min(point[1] for point in track)
    max_y = max(point[1] for point in track)

    # Calculate scale factors
    scale_x = (screen_width - 2 * margin) / (max_x - min_x)
    scale_y = (screen_height - 2 * margin) / (max_y - min_y)
    scale = min(scale_x, scale_y)  # Maintain aspect ratio

    # Scale and translate the points
    scaled_track = [
        (
            int((point[0] - min_x) * scale + margin),
            int((point[1] - min_y) * scale + margin)
        )
        for point in track
    ]
    return scaled_track

def get_interpolated_position(track, progress):
    """
    Calculate the interpolated position of a driver on the track.
    :param track: List of waypoints defining the track.
    :param progress: Progress value (0.0 to 1.0) along the track.
    :return: Interpolated (x, y) position.
    """
    total_segments = len(track)
    segment_index = int(progress * total_segments) % total_segments
    next_segment_index = (segment_index + 1) % total_segments

    # Current and next waypoints
    current_point = track[segment_index]
    next_point = track[next_segment_index]

    # Calculate local progress within the segment
    segment_progress = (progress * total_segments) - segment_index

    # Interpolate between the two waypoints
    x = current_point[0] + (next_point[0] - current_point[0]) * segment_progress
    y = current_point[1] + (next_point[1] - current_point[1]) * segment_progress

    return int(x), int(y)