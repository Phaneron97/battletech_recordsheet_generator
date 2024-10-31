from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from PIL import Image
import os

# Register the custom fonts
pdfmetrics.registerFont(TTFont('EurostileBold', 'fonts/EurostileBold.ttf'))
pdfmetrics.registerFont(TTFont('Eurostile', 'fonts/Eurostile.ttf'))

def create_filled_pdf(custom_mech, custom_pdf, output_filename, template_filename):
    # Delete the existing filled_record_sheet.pdf if it exists
    if os.path.exists(output_filename):
        os.remove(output_filename)

    # Temporary filename for intermediate content
    temp_filename = "temp_content.pdf"
    
    # Create a new PDF to add text and images
    c = canvas.Canvas(temp_filename, pagesize=letter)
    
    # Add each item from the custom_mech to the canvas using the custom_pdf
    for key, value in custom_mech.items():
        if key in custom_pdf:
            data = custom_pdf[key]
            c.setFont(data['font'], data['size'])
            c.drawString(data['x'], letter[1] - data['y'], value)  # Adjust y-coordinate for reportlab origin

    # Add the mech image
    mech_type = custom_mech.get("type")
    if mech_type:
        image_info = custom_pdf["mech_image"]
        image_path = os.path.join("mech_images", f"{mech_type}.webp")
        if os.path.exists(image_path):
            with Image.open(image_path) as img:
                # Crop the image to the required aspect ratio
                img_width, img_height = img.size
                aspect_ratio = image_info['width'] / image_info['height']
                new_width = img_width
                new_height = int(img_width / aspect_ratio)

                if new_height > img_height:
                    new_height = img_height
                    new_width = int(img_height * aspect_ratio)

                left = (img_width - new_width) / 2
                top = (img_height - new_height) / 2
                right = (img_width + new_width) / 2
                bottom = (img_height + new_height) / 2

                img_cropped = img.crop((left, top, right, bottom))
                img_cropped_reader = ImageReader(img_cropped)
                c.drawImage(img_cropped_reader, image_info['x'], letter[1] - image_info['y'] - image_info['height'], 
                            width=image_info['width'], height=image_info['height'])

    # Add the empty armor diagram
    # add_empty_armor_diagram(c, custom_pdf["armor_diagram"])

    # Add armor points to the armor diagram
    add_armor_points(c, custom_pdf["armor_diagram"], custom_mech["armor_points"])

    c.save()
    
    # Merge the new content on top of the existing template
    template = PdfReader(template_filename)
    new_content = PdfReader(temp_filename)
    writer = PdfWriter()
    for page_num in range(len(template.pages)):
        page = template.pages[page_num]
        if page_num < len(new_content.pages):
            new_page = new_content.pages[page_num]
            page.merge_page(new_page)
        writer.add_page(page)
    
    with open(output_filename, 'wb') as out:
        writer.write(out)

    # Clean up the temporary file
    os.remove(temp_filename)

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

# Example dictionaries
custom_pdf = {
    "type": {
        "x": 70.0,
        "y": 147,
        "font": "EurostileBold",
        "size": 10
    },
    "tonnage": {
        "x": 190,
        "y": 160,
        "font": "Eurostile",
        "size": 10
    },
    "mech_image": {
        "x": 249,
        "y": 198,
        "width": 145,
        "height": 202
    },
    "armor_diagram": {
        "x": 396,
        "y": 78,
        "width": 180,
        "height": 317,
        "head": {
            "x": 396,
            "y": 78,
            "width": 30,
            "height": 30
        },
        "center_torso": {
            "x": 426,
            "y": 78,
            "width": 60,
            "height": 60
        },
        "left_torso": {
            "x": 486,
            "y": 78,
            "width": 45,
            "height": 60
        },
        "right_torso": {
            "x": 10,
            "y": 10,
            "width": 100,
            "height": 100
        }
    }
}

custom_mech = {
    "type": "BattleMaster BLR-1G",
    "tonnage": "85",
    "armor_points": {
        "head": 6,
        "center_torso": 10,
        "left_torso": 8,
        "right_torso": 8
    }
}

output_filled_pdf = "filled_record_sheet.pdf"
template_pdf = "blank_record_sheet.pdf"
create_filled_pdf(custom_mech, custom_pdf, output_filled_pdf, template_pdf)
