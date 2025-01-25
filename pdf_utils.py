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


def add_placeholder_diagram(c, armor_diagram_info, image_name):
    """Draws the image with a border for debugging."""
    image_path = os.path.join("sheet_images", image_name)
    
    # Calculate the position of the image
    x_position = armor_diagram_info['x']
    y_position = letter[1] - armor_diagram_info['y'] - armor_diagram_info['height']
    
    # Draw the image (assuming the image exists)
    c.drawImage(ImageReader(image_path), x_position, y_position, 
                width=armor_diagram_info['width'], height=armor_diagram_info['height'])
    
    # Draw a border around the image for debugging purposes
    # c.setStrokeColor(red)  # Set the color of the border (red)
    # c.setLineWidth(2)      # Set the border line width
    # c.rect(x_position, y_position, armor_diagram_info['width'], armor_diagram_info['height'])


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


def populate_critical_hit_table(c, custom_mech, critical_hit_table):
    """
    Populates the critical hit table with weapons, heat sinks, and ammo.
    Items that take up multiple slots will occupy the required number of consecutive slots.
    Remaining slots are filled with 'Roll Again', while respecting reserved and actuator-occupied slots.
    """
    # Helper to write text to a critical slot
    def write_to_slot(slot_info, text, slot_key):
        print(f"Writing '{text}' to slot {slot_key} {slot_info}")
        c.setFont(slot_info["font"], slot_info["size"])
        c.drawString(slot_info["x"], letter[1] - slot_info["y"], text)

    # Iterate over each component in the critical hit table
    for component, slots in critical_hit_table.items():
        print(f"Processing component: {component}")

        # Separate reserved and free slots
        reserved_slots = {k: v for k, v in slots.items() if v.get("reserved", False)}
        free_slots = {k: v for k, v in slots.items() if not v.get("reserved", False)}

        print(f"Reserved slots: {reserved_slots.keys()}")
        print(f"Free slots: {free_slots.keys()}")

        # Track which free slots have been used
        used_slot_keys = set()

        # Check for actuators or other components that occupy slots
        if component in ["left_arm", "right_arm"]:
            # Check for actuators in custom_mech
            arm_parts = custom_mech["mech_data"].get(f"{component}_parts", {})
            for part, is_present in arm_parts.items():
                if is_present:
                    # Find the slot occupied by the actuator and mark it as used
                    for slot_key, slot_info in slots.items():
                        if part in slot_info:  # Slot is used by the actuator
                            print(f"{component}: Slot {slot_key} occupied by {part}")
                            used_slot_keys.add(slot_key)

        # Place weapons
        weapons = custom_mech["weapons"].get(component, {})
        for weapon_name, quantity in weapons.items():
            for _ in range(quantity):
                # Find the next available free slot(s)
                slots_required = get_slots_required(weapon_name)  # Function to determine how many slots are required
                free_slot_keys = [slot_key for slot_key in free_slots.keys() if slot_key not in used_slot_keys]

                if len(free_slot_keys) >= slots_required:
                    for i in range(slots_required):
                        slot_key = free_slot_keys[i]
                        slot_info = free_slots[slot_key]
                        write_to_slot(slot_info, weapon_name, slot_key)
                        used_slot_keys.add(slot_key)
                else:
                    print(f"Not enough slots available in {component} for {weapon_name}.")
                    break

        # Place heat sinks
        heatsinks = custom_mech["heatsinks"]["heatsink_locations"].get(component, 0)
        for _ in range(heatsinks):
            # Heat sinks take 1 slot each
            free_slot_keys = [slot_key for slot_key in free_slots.keys() if slot_key not in used_slot_keys]

            if free_slot_keys:
                slot_key = free_slot_keys[0]
                slot_info = free_slots[slot_key]
                write_to_slot(slot_info, "Heat Sink", slot_key)
                used_slot_keys.add(slot_key)
            else:
                print(f"No more slots available in {component} for heat sinks.")
                break

        # Place ammunition
        ammo = custom_mech["ammunition"].get(component, {})
        for ammo_type, quantity in ammo.items():
            for _ in range(quantity):
                # Ammo takes 1 slot each
                free_slot_keys = [slot_key for slot_key in free_slots.keys() if slot_key not in used_slot_keys]

                if free_slot_keys:
                    slot_key = free_slot_keys[0]
                    slot_info = free_slots[slot_key]
                    write_to_slot(slot_info, f"Ammo ({ammo_type})", slot_key)
                    used_slot_keys.add(slot_key)
                else:
                    print(f"No more slots available in {component} for ammo.")
                    break

        # Fill remaining free slots with "Roll Again"
        for slot_key, slot_info in free_slots.items():
            if slot_key not in used_slot_keys:
                write_to_slot(slot_info, "Roll Again", slot_key)
                used_slot_keys.add(slot_key)


def get_slots_required(weapon_name):
    """
    Returns the number of critical slots required for a given weapon.
    This function should refer to a predefined dictionary or logic
    mapping weapon names to their critical slot usage.
    """
    weapon_slots = {
        "PPC": 3,  # PPC takes 3 slots
        "Machine_Gun": 1,  # Machine Gun takes 1 slot
        "Medium_Laser": 1,  # Medium Laser takes 1 slot
        "SRM_6": 2,  # SRM-6 takes 2 slots
        # Add other weapons as needed
    }
    return weapon_slots.get(weapon_name, 1)  # Default to 1 slot if weapon is not found


def draw_debug_grid(c, page_width, page_height, grid_size=100):
    """
    Draws a blue dotted grid over the entire PDF page and adds coordinate labels at each intersection.
    
    Args:
        c: The canvas object.
        page_width: Width of the page in points.
        page_height: Height of the page in points.
        grid_size: Size of each grid cell in points (default is 100).
    """
    c.setStrokeColorRGB(0, 0, 1)  # Set stroke color to blue
    c.setDash(3, 3)  # Set line style to dotted (3 points on, 3 points off)
    c.setFillColorRGB(0, 0, 1)
    c.setFont("Helvetica", 10)  # Set font for coordinate labels

    # Draw vertical lines and annotate coordinates
    for x in range(0, int(page_width), grid_size):
        c.line(x, 0, x, page_height)  # Draw the vertical line
        for y in range(0, int(page_height), grid_size):
            # Add a coordinate label at each grid intersection
            c.drawString(x + 2, page_height - y - 10, f"({x},{y})")  # Adjust positioning for clarity
    
    # Draw horizontal lines
    for y in range(0, int(page_height), grid_size):
        c.line(0, y, page_width, y)  # Draw the horizontal line

    # Reset canvas settings
    c.setDash(1, 0)  # Solid lines after this function


def create_filled_pdf(custom_mech, custom_pdf, output_filename, template_filename, weapon_details):
    print("weapon_details", weapon_details)

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
    page_width, page_height = letter

    # Get custom mech
    custom_mech_info = custom_mech["mech_data"]
    set_text_from_layout_data(c, custom_mech["mech_data"], custom_pdf["mech_data"])
        
    # Add custom mech image
    mech_type = custom_mech_info.get("type")
    if mech_type:
        add_mech_image(c, mech_type, custom_pdf["mech_image"])
        
    c.setFont("Eurostile", 9)  # Set font for weapon details
    # Add the placeholder diagrams for armor and weapons
    add_placeholder_diagram(c, custom_pdf["armor_diagram"], "armor_diagram_empty.png")
    add_placeholder_diagram(c, custom_pdf["structure_diagram"], "structure_diagram_empty.png")
    add_placeholder_diagram(c, custom_pdf["mech_data"]["weapons_and_equipment_inv_empty_placeholder"], "empty_weapons_and_equipment_inv.png")
    add_placeholder_diagram(c, custom_pdf["heat_data"]["heat_data_diagram"], "empty_heat_data_diagram.png")
    add_placeholder_for_arm_parts(c, custom_mech, custom_pdf)
    add_armor_points(c, custom_pdf["armor_diagram"], custom_mech["armor_points"])
    add_armor_points(c, custom_pdf["structure_diagram"], custom_mech["structure_points"])
    populate_critical_hit_table(c, custom_mech, custom_pdf["critical_hit_table"])

    # Calculate total heat sinks
    add_heat_points(c, custom_pdf["heat_data"], calculate_amount_heatsinks(custom_mech))

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

    # Draw a debug grid to aid with positioning
    draw_debug_grid(c, page_width, page_height)

    
    # Calculate mech BV
    mech_bv = calculate_battle_value(custom_mech, weapon_details)
    print(f"Mech BV: {mech_bv}")

    # Add mech BV to PDF
    bv_settings = custom_pdf.get("bv", {})
    print("bv_settings", bv_settings)
    if bv_settings:
        c.setFont(bv_settings["font"], bv_settings["size"])
        c.drawString(bv_settings["x"], letter[1] - bv_settings["y"], str(mech_bv))

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