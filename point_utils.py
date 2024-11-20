from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import os
import math
from reportlab.lib.colors import red  # Import a color for the border

def add_armor_points(c, armor_diagram_info, armor_points):
    # Define the radius of the circles representing armor points
    circle_radius = 2
    
    # Function to draw circles in a grid pattern within a given area
    def draw_circles(x_start, y_start, width, height, num_points, rotation, margin):
        # Calculate the available width and height after applying margins
        available_width = width - 2 * margin
        available_height = height - 2 * margin

        # Calculate the optimal number of columns and rows based on the circle diameter
        circle_diameter = 2 * circle_radius
        cols = int(available_width // circle_diameter)
        rows = int(math.ceil(num_points / cols))

        # Adjust grid size to ensure all points appear within the given available width and height
        x_spacing = available_width / max(cols - 1, 1)
        y_spacing = available_height / max(rows - 1, 1)

        # Center the grid within the component with margins
        x_offset = x_start + margin
        y_offset = y_start - margin

        # Rotate and draw the circles in the grid
        for row in range(rows):
            points_in_row = cols if row < rows - 1 else num_points % cols or cols
            row_offset = (available_width - (points_in_row - 1) * x_spacing) / 2

            for col in range(points_in_row):
                # Calculate x and y positions with centering offsets and margins
                x = x_offset + col * x_spacing + row_offset
                y = y_offset - row * y_spacing

                # Apply rotation
                rad = math.radians(rotation)
                x_rot = math.cos(rad) * (x - x_start) - math.sin(rad) * (y - y_start) + x_start
                y_rot = math.sin(rad) * (x - x_start) + math.cos(rad) * (y - y_start) + y_start

                c.circle(x_rot, y_rot, circle_radius, fill=0)
    
    # Draw debugging rectangles and circles for each component based on the armor_points dictionary
    for component, points in armor_points.items():
        if component in armor_diagram_info:
            comp_info = armor_diagram_info[component]
            # Draw the bounding rectangle for debugging
            c.setStrokeColorRGB(1, 0, 0)  # Red color for the bounding box
            c.rect(
                comp_info['x'], 
                letter[1] - comp_info['y'] - comp_info['height'], 
                comp_info['width'], 
                comp_info['height'], 
                stroke=1, 
                fill=0)
            draw_circles(
                comp_info['x'], 
                letter[1] - comp_info['y'], 
                comp_info['width'], 
                comp_info['height'], 
                points, 
                comp_info.get('rotation', 0), 
                comp_info.get('margin', 0))


def add_heat_points(c, heat_data_info, total_heatsinks):
    """Adds heat sink points based on the calculated total heat sinks, using the 'heat_data_diagram' layout."""
    circle_radius = 3  # Radius for each heat sink point circle
    
    def draw_circles(x_start, y_start, width, height, num_points, rotation, margin):
        """Draws circles in a grid layout to represent heat sinks."""
        available_width = width - 2 * margin
        available_height = height - 2 * margin
        circle_diameter = 2 * circle_radius
        cols = int(available_width // circle_diameter)
        rows = int(math.ceil(num_points / cols))

        x_spacing = available_width / max(cols - 1, 1)
        y_spacing = available_height / max(rows - 1, 1)

        x_offset = x_start + margin
        y_offset = y_start - margin

        for row in range(rows):
            points_in_row = cols if row < rows - 1 else num_points % cols or cols
            row_offset = (available_width - (points_in_row - 1) * x_spacing) / 2

            for col in range(points_in_row):
                x = x_offset + col * x_spacing + row_offset
                y = y_offset - row * y_spacing

                rad = math.radians(rotation)
                x_rot = math.cos(rad) * (x - x_start) - math.sin(rad) * (y - y_start) + x_start
                y_rot = math.sin(rad) * (x - x_start) + math.cos(rad) * (y - y_start) + y_start

                c.circle(x_rot, y_rot, circle_radius, fill=0)

    heat_info = heat_data_info.get("heat_data_diagram", {})
    if heat_info:
        draw_circles(
            heat_info["x"],
            letter[1] - heat_info["y"],
            heat_info["width"],
            heat_info["height"],
            total_heatsinks,
            heat_info.get("rotation", 0),
            heat_info.get("margin", 0)
        )