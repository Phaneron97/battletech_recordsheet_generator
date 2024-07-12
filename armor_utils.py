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
    circle_radius = 5
    
    # Function to draw circles in a grid pattern within a given area
    def draw_circles(x_start, y_start, width, height, num_points):
        rows = int(height / (2 * circle_radius))
        cols = int(width / (2 * circle_radius))
        for i in range(num_points):
            row = i // cols
            col = i % cols
            if row < rows:
                x = x_start + col * 2 * circle_radius
                y = y_start - row * 2 * circle_radius
                c.circle(x, y, circle_radius, fill=1)
    
    # Draw circles for each component based on the armor_points dictionary
    for component, points in armor_points.items():
        if component in armor_diagram_info:
            comp_info = armor_diagram_info[component]
            draw_circles(comp_info['x'], letter[1] - comp_info['y'], comp_info['width'], comp_info['height'], points)
