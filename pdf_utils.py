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

def create_filled_pdf(mech_data, layout_info, output_filename, template_filename):
    # Delete the existing filled_record_sheet.pdf if it exists
    if os.path.exists(output_filename):
        os.remove(output_filename)

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