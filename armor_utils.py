from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import os

def add_empty_armor_diagram(c, armor_diagram_info):    
    # Print empty armor diagram
    image_path = os.path.join("sheet_images", "armor_diagram_empty.png")
    if os.path.exists(image_path):
        c.drawImage(ImageReader(image_path), armor_diagram_info['x'], letter[1] - armor_diagram_info['y'] - armor_diagram_info['height'], 
                    width=armor_diagram_info['width'], height=armor_diagram_info['height'])

def add_armor_points(c, armor_diagram_info, armor_points):
    # Define the radius of the circles representing armor points
    circle_radius = 3
    
    # Function to draw circles in a grid pattern within a given area
    def draw_circles(x_start, y_start, width, height, num_points):
        # Calculate the number of rows and columns based on the number of points
        cols = int((num_points ** 0.5) + 0.5)
        rows = int((num_points / cols) + 0.5)
        
        # Adjust grid size to ensure all points appear within the given width and height
        grid_width = width / max(cols, 1)
        grid_height = height / max(rows, 1)
        
        # Calculate the spacing between circles
        x_spacing = grid_width if grid_width < grid_height else grid_height
        y_spacing = x_spacing
        
        # Draw the circles in the grid
        for i in range(num_points):
            row = i // cols
            col = i % cols
            x = x_start + col * x_spacing + x_spacing / 2
            y = y_start - row * y_spacing - y_spacing / 2
            c.circle(x, y, circle_radius, fill=0)
    
    # Draw circles for each component based on the armor_points dictionary
    for component, points in armor_points.items():
        if component in armor_diagram_info:
            comp_info = armor_diagram_info[component]
            draw_circles(comp_info['x'], letter[1] - comp_info['y'], comp_info['width'], comp_info['height'], points)
