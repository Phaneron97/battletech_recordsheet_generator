from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from PIL import Image
import os
from armor_utils import add_empty_armor_diagram, add_armor_points

# Register the custom fonts
pdfmetrics.registerFont(TTFont('EurostileBold', 'fonts/EurostileBold.ttf'))
pdfmetrics.registerFont(TTFont('Eurostile', 'fonts/Eurostile.ttf'))

def create_filled_pdf(mech_data, layout_info, output_filename, template_filename, weapon_details):
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Delete the existing PDF file if it exists
    if os.path.exists(output_filename):
        print(f"Deleting old file: {output_filename}")
        os.remove(output_filename)
    else:
        print(f"File {output_filename} does not exist, creating a new one.")

    # Temporary filename for intermediate content
    temp_filename = "temp_content.pdf"
    
    # Create a new PDF to add text and images
    c = canvas.Canvas(temp_filename, pagesize=letter)

    # Add each item from the mech_data to the canvas using the layout_info
    for key, value in mech_data.items():
        if key in layout_info:
            data = layout_info[key]
            c.setFont(data['font'], data['size'])
            c.drawString(data['x'], letter[1] - data['y'], value)  # Adjust y-coordinate for reportlab origin

    # Add the mech image
    mech_type = mech_data.get("type")
    if mech_type:
        image_info = layout_info["mech_image"]
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
    add_empty_armor_diagram(c, layout_info["armor_diagram"])

    # Add armor points to the armor diagram
    add_armor_points(c, layout_info["armor_diagram"], mech_data["armor_points"])

    # Add weapon details below each other in columns
    start_y = 560
    x_quantity = 48
    x_name = 60
    x_location = 118
    x_heat = 134
    x_damage = 148
    x_min = 185
    x_sht = 199
    x_med = 215
    x_lng = 231

    c.setFont("Eurostile", 9)  # Set font for weapon details
    for weapon in weapon_details:
        c.drawString(x_quantity, start_y, str(weapon['quantity']))
        c.drawString(x_name, start_y, weapon['name'])
        c.drawString(x_location, start_y, weapon['location'])
        c.drawString(x_heat, start_y, str(weapon['heat']))
        c.drawString(x_damage, start_y, str(weapon['damage']))
        c.drawString(x_min, start_y, str(weapon['min']))
        c.drawString(x_sht, start_y, str(weapon['sht']))
        c.drawString(x_med, start_y, str(weapon['med']))
        c.drawString(x_lng, start_y, str(weapon['lng']))
        start_y -= 11  # Move down for the next weapon

    # Save the canvas
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
    
    # Write the final PDF to the output file
    with open(output_filename, 'wb') as out:
        writer.write(out)

    # Clean up the temporary file
    os.remove(temp_filename)

