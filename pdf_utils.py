from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from PIL import Image
import os
from armor_utils import add_placeholder_diagram, add_armor_points
import math
import csv

# Register the custom fonts
pdfmetrics.registerFont(TTFont('EurostileBold', 'fonts/EurostileBold.ttf'))
pdfmetrics.registerFont(TTFont('Eurostile', 'fonts/Eurostile.ttf'))

# Load weapon data from CSV
def load_weapon_data(csv_filename):
    weapon_data = {}
    with open(csv_filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            weapon_name = row["Name"].lower().replace(" ", "_")
            weapon_data[weapon_name] = {
                "damage": int(row["Dmg"]),
                "heat": int(row["Ht"])
            }
    return weapon_data

# Calculate Battle Value (BV)
def calculate_battle_value(custom_mech, weapon_data):
    def calculate_armor_factor(armor_points, armor_type_modifier=1.0):
        total_armor = sum(armor_points.values())
        return total_armor * 2.5 * armor_type_modifier

    def calculate_internal_structure_points(structure_points, structure_type_modifier=1.0, engine_modifier=1.0):
        total_structure_points = sum(structure_points.values())
        return total_structure_points * 1.5 * structure_type_modifier * engine_modifier

    # Defensive Battle Rating (DBR)
    armor_points = custom_mech["armor_points"]
    structure_points = custom_mech["structure_points"]

    armor_factor = calculate_armor_factor(armor_points)
    structure_factor = calculate_internal_structure_points(structure_points)
    mech_tonnage = int(custom_mech["mech_data"]["tonnage"])
    gyro_modifier = 0.5
    gyro_bv = mech_tonnage * gyro_modifier
    defensive_battle_rating = (armor_factor + structure_factor + gyro_bv) * 1.2

    # Offensive Battle Rating (OBR)
    weapon_bv_total = 0
    for location, weapons in custom_mech["weapons"].items():
        for weapon_name, quantity in weapons.items():
            weapon_name_key = weapon_name.lower().replace(" ", "_")
            if weapon_name_key in weapon_data:
                damage = weapon_data[weapon_name_key]["damage"]
                heat = weapon_data[weapon_name_key]["heat"]
                weapon_bv = damage * heat
                weapon_bv_total += weapon_bv * quantity

    # Speed Factor based on movement points
    movement_points = custom_mech["mech_data"]["movement_points"]
    running_speed = int(movement_points["running"])
    speed_factor = running_speed / 5

    offensive_battle_rating = weapon_bv_total * speed_factor

    # Final BV Calculation
    total_bv = defensive_battle_rating + offensive_battle_rating
    final_bv = math.ceil(total_bv)

    return final_bv


def set_text_from_layout_data(c, mech_data, layout_data):
    """Draws mech data onto the PDF canvas, including both top-level and nested data items."""
    for key, data in mech_data.items():
        if key in layout_data:
            info = layout_data[key]
            if isinstance(data, dict):
                # Handle nested dictionaries (e.g., movement points)
                for sub_key, sub_value in data.items():
                    if sub_key in layout_data[key]:
                        sub_info = layout_data[key][sub_key]
                        c.setFont(sub_info['font'], sub_info['size'])
                        c.drawString(sub_info['x'], letter[1] - sub_info['y'], str(sub_value))
            else:
                # Handle top-level values (e.g., type and tonnage)
                c.setFont(info['font'], info['size'])
                c.drawString(info['x'], letter[1] - info['y'], str(data))

def add_mech_image(c, mech_type, image_info, image_folder="mech_images"):
    """Adds a mech image to the PDF canvas, cropping and scaling it to fit the specified dimensions."""
    image_path = os.path.join(image_folder, f"{mech_type}.webp")
    if os.path.exists(image_path):
        with Image.open(image_path) as img:
            img_width, img_height = img.size
            aspect_ratio = image_info['width'] / image_info['height']
            new_width = img_width
            new_height = int(img_width / aspect_ratio)

            # Adjust dimensions to maintain the aspect ratio
            if new_height > img_height:
                new_height = img_height
                new_width = int(img_height * aspect_ratio)

            # Calculate cropping box to center the image
            left = (img_width - new_width) / 2
            top = (img_height - new_height) / 2
            img_cropped = img.crop((left, top, left + new_width, top + new_height))

            # Draw the cropped image on the canvas
            img_cropped_reader = ImageReader(img_cropped)
            c.drawImage(
                img_cropped_reader,
                image_info['x'],
                letter[1] - image_info['y'] - image_info['height'],
                width=image_info['width'],
                height=image_info['height']
            )
    else:
        print(f"Image not found for mech type '{mech_type}' at '{image_path}'")

def add_tech_base_checkmark(c, tech_base, tech_base_checkmark):
    """Draws a checkmark for the tech base (IS or Clan) based on tech_base value."""
    checkmark_image = "sheet_images/checkmark.png"
    # Get the position based on tech_base
    pos = tech_base_checkmark.get(tech_base, tech_base_checkmark["IS"])

    # Draw the checkmark image at the specified position
    if os.path.exists(checkmark_image):
        c.drawImage(ImageReader(checkmark_image), pos["x"], letter[1] - pos["y"], width=6, height=6)

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

    # Add armor points
    add_armor_points(c, custom_pdf["armor_diagram"], custom_mech["armor_points"])
    add_armor_points(c, custom_pdf["structure_diagram"], custom_mech["structure_points"])

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
    add_tech_base_checkmark(c, custom_mech_info.get("tech_base", "IS"), custom_pdf["tech_base_checkmark"])

    # Load weapon data and calculate BV
    weapon_csv = "weapons.csv"
    weapon_data = load_weapon_data(weapon_csv)
    print("Battlevalue: ", calculate_battle_value(custom_mech, weapon_data))

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
