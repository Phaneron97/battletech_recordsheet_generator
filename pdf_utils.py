from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from PIL import Image
import os
from point_utils import *
from mech_utils import *

# Register the custom fonts
pdfmetrics.registerFont(TTFont('EurostileBold', 'fonts/EurostileBold.ttf'))
pdfmetrics.registerFont(TTFont('Eurostile', 'fonts/EuroStile.ttf'))


def add_checkmark(c, entity_type, entity_checkmark, custom_mech=None):
    """Draws a checkmark based on the given entity type (tech base or heatsink type)."""
    checkmark_image = "sheet_images/checkmark.png"
    
    # Ensure custom_mech is provided if needed
    if custom_mech is None:
        raise ValueError("custom_mech must be provided")

    # Initialize the position variable
    pos = None

    # Handle 'tech_base' case
    if entity_type == 'tech_base':
        # Get the tech_base from custom_mech (default to 'IS' if not present)
        tech_base = custom_mech["mech_data"].get("tech_base", "IS")
        
        # Get the position from entity_checkmark based on the tech_base value
        pos = entity_checkmark.get(tech_base)
        
    # Handle 'heatsink_type' case
    elif entity_type == 'heatsink_type':
        # Get the heatsink_type from custom_mech (default to 'single' if not present)
        heatsink_type = custom_mech["heatsinks"].get("heatsink_type", "single")
        
        # Get the position from entity_checkmark based on the heatsink_type value
        pos = entity_checkmark.get(heatsink_type)
    
    else:
        # Raise an error if an unsupported entity_type is passed
        raise ValueError("Unsupported entity_type. Must be 'tech_base' or 'heatsink_type'.")

    # If the position is valid and the checkmark image exists, draw the checkmark
    if pos and os.path.exists(checkmark_image):
        c.drawImage(ImageReader(checkmark_image), pos["x"], letter[1] - pos["y"], width=6, height=6)
    else:
        raise ValueError(f"Position not found for entity_type '{entity_type}' or invalid checkmark image path.")



def create_filled_pdf(custom_mech, custom_pdf, output_filename, template_filename, weapon_details):
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Delete the existing PDF file if it exists
    if os.path.exists(output_filename):
        print(f"Deleting old file: {output_filename}")
        os.remove(output_filename)

    # Temporary filename for intermediate content
    temp_filename = "temp_content.pdf"
    
    # Create a new PDF to add text and images
    c = canvas.Canvas(temp_filename, pagesize=letter)

    # Get custom mech
    custom_mech_info = custom_mech["mech_data"]
    set_text_from_layout_data(c, custom_mech["mech_data"], custom_pdf["mech_data"])
        
    # Add custom mech image
    mech_type = custom_mech_info.get("type")
    if mech_type:
        add_mech_image(c, mech_type, custom_pdf["mech_image"])

    # Add the placeholder diagrams for armor and weapons
    add_placeholder_diagram(c, custom_pdf["armor_diagram"], "armor_diagram_empty.png")
    add_placeholder_diagram(c, custom_pdf["structure_diagram"], "structure_diagram_empty.png")
    add_placeholder_diagram(c, custom_pdf["mech_data"]["weapons_and_equipment_inv_empty_placeholder"], "empty_weapons_and_equipment_inv.png")
    add_placeholder_diagram(c, custom_pdf["heat_data"]["heat_data_diagram"], "empty_heat_data_diagram.png")
    add_placeholder_for_arm_parts(c, custom_mech, custom_pdf)
    add_armor_points(c, custom_pdf["armor_diagram"], custom_mech["armor_points"])
    add_armor_points(c, custom_pdf["structure_diagram"], custom_mech["structure_points"])

    # Calculate total heat sinks
    total_heatsinks = calculate_total_heatsinks(custom_mech)

    # Draw the heat sink points on the canvas
    add_heat_points(c, custom_pdf["heat_data"], total_heatsinks)

    # Add weapons and equipment
    start_y = custom_pdf["mech_data"]["weapons_and_equipment_inv_text"]["y"]
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

    # Add tech base checkmark
    add_checkmark(c, 'tech_base', custom_pdf["tech_base_checkmark"], custom_mech)
    # Add heatsink type checkmark
    add_checkmark(c, 'heatsink_type', custom_pdf["heat_data"], custom_mech)

    # Load weapon data and calculate BV
    weapon_csv = "weapons_and_ammo.csv"
    weapon_data = load_weapon_data(weapon_csv)

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