from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from PIL import Image
import os
import math
import csv
import re

# Load weapon data from CSV and clean the "Damage" and "Heat" columns
# def load_weapon_data(csv_filename):
#     weapon_data = {}
    
#     with open(csv_filename, mode='r', newline='') as file:
#         reader = csv.DictReader(file)
        
#         for row in reader:
#             # Normalize the weapon name for consistent lookup
#             weapon_name = row["Weapon/Item"].strip().lower().replace(" ", "_")
            
#             # Extract primary damage and heat values by removing the trailing "(x)" part if present
#             damage = re.sub(r'\s*\(.*\)$', '', row["Damage"]).strip()
#             heat = re.sub(r'\s*\(.*\)$', '', row["Heat"]).strip()
            
#             # Convert damage and heat to integers where applicable
#             weapon_data[weapon_name] = {
#                 "damage": int(damage) if damage.isdigit() else damage,
#                 "heat": int(heat) if heat.isdigit() else heat
#             }
    
#     # print(weapon_data)
#     return weapon_data


# Calculate Battle Value (BV)
def calculate_battle_value(custom_mech, weapon_data):
    """
    Calculates the Battle Value (BV) of a mech, considering armor, structure, weapons,
    ammunition, and movement points.
    """

    # Step 1: Defensive Battle Rating (DBR)
    def calculate_armor_factor(armor_points, armor_type_modifier=1.0):
        """Calculates the armor factor based on total armor points and a type modifier."""
        total_armor = sum(armor_points.values())
        return total_armor * 2.5 * armor_type_modifier

    def calculate_internal_structure_points(structure_points, structure_type_modifier=1.0, engine_modifier=1.0):
        """Calculates the structure factor based on structure points, modifiers, and engine type."""
        total_structure_points = sum(structure_points.values())
        return total_structure_points * 1.5 * structure_type_modifier * engine_modifier

    # Extract armor and structure data
    armor_points = custom_mech["armor_points"]
    structure_points = custom_mech["structure_points"]
    mech_tonnage = int(custom_mech["mech_data"]["tonnage"])

    # Calculate factors for DBR
    armor_factor = calculate_armor_factor(armor_points)
    structure_factor = calculate_internal_structure_points(structure_points)
    gyro_modifier = 0.5
    gyro_bv = mech_tonnage * gyro_modifier

    # Defensive Battle Rating (DBR)
    defensive_battle_rating = (armor_factor + structure_factor + gyro_bv) * 1.2

    # Print debug information for DBR
    # print("Armor Factor:", armor_factor)
    # print("Structure Factor:", structure_factor)
    # print("Gyro BV:", gyro_bv)
    # print("Defensive Battle Rating:", defensive_battle_rating)

    # Step 2: Offensive Battle Rating (OBR)
    weapon_bv_total = 0
    for location, weapons in custom_mech["weapons"].items():
        for weapon_name, quantity in weapons.items():
            # Normalize weapon name for lookup and retrieve stats
            weapon_name_key = weapon_name.lower().replace(" ", "_")
            if weapon_name_key in weapon_data:
                damage = weapon_data[weapon_name_key]["damage"]

                heat = weapon_data[weapon_name_key]["heat"]
                weapon_bv = damage * heat  # BV calculation per weapon instance
                # print("damage", damage)
                # print("heat", heat)
                # print("weaponbv",weapon_bv)
                
                # Convert quantity to integer before multiplication
                weapon_bv_total += weapon_bv * int(quantity)

    # Speed Factor based on movement points
    movement_points = custom_mech["mech_data"]["movement_points"]
    running_speed = int(movement_points["running"])
    speed_factor = running_speed / 5

    offensive_battle_rating = weapon_bv_total * speed_factor

    # Print debug information for OBR
    print("Weapon BV Total:", weapon_bv_total)
    print("Speed Factor:", speed_factor)
    print("Offensive Battle Rating:", offensive_battle_rating)

    # Step 3: Ammunition Penalty (per ton of explosive ammo in critical locations or without CASE protection)
    ammo_penalty = 0
    critical_locations = ["center_torso", "head", "left_leg", "right_leg"]

    for location, ammo in custom_mech.get("ammunition", {}).items():
        for ammo_type, tonnage in ammo.items():
            # Check if location is critical or lacks CASE protection
            if location in critical_locations or not custom_mech.get("case_protection", {}).get(location, False):
                ammo_penalty += 15 * tonnage  # 15 points per ton of explosive ammo

    # Print debug information for Ammo Penalty
    print("Ammunition Penalty:", ammo_penalty)

    # Step 4: Final BV Calculation - Total up DBR, OBR, and subtract ammo penalty
    total_bv = max(1, defensive_battle_rating + offensive_battle_rating - ammo_penalty)  # Ensure BV is at least 1
    final_bv = math.ceil(total_bv)

    # Print Final Battle Value
    print("Total Battle Value:", final_bv)

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


def find_closest_image(mech_type, image_folder):
    """Finds the exact image file in the image folder based on the mech type, case-insensitive."""
    mech_type_lower = mech_type.lower()

    # Debug: Print directory contents
    # print(f"Searching for '{mech_type}' in '{image_folder}'")
    # print("Directory contents:", os.listdir(image_folder))  # List all files in the directory

    # Search through the folder for an exact case-insensitive match
    for file_name in os.listdir(image_folder):
        file_base_name, file_ext = os.path.splitext(file_name)

        # Debug: Print each file being checked
        # print(f"Checking file: '{file_base_name}{file_ext}' against '{mech_type}'")

        # Check if the lowercase file name matches the mech type exactly
        if file_base_name.lower() == mech_type_lower:
            full_path = os.path.join(image_folder, file_name)
            print(f"Image match found: {full_path}")  # Debug line for match confirmation
            return full_path

    # If no match is found, print debug message
    print(f"No image match found for '{mech_type}' in '{image_folder}'")
    return None


def add_mech_image(c, mech_type, image_info, image_folder="mech_images/megamek_images/Mech"):
    """Adds a mech image to the PDF canvas, cropping and scaling it to fit the specified dimensions."""
    # Find the closest image match based on mech_type
    image_path = find_closest_image(mech_type, image_folder)
    
    if image_path and os.path.exists(image_path):
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
        print(f"Image not found for mech type '{mech_type}' in '{image_folder}'")


def get_engine_rating(mech_tonnage, walking_mp):
    """See techmanual p.48 for calculation"""
    return math.ceil(mech_tonnage * walking_mp)
    

def get_internal_heatsinks(engine_rating):
    """calculate amount of internal heatsinks based on engine_rating, always rounds number down. returns one integer"""
    return math.floor(engine_rating / 25)


def get_running_mp(walking_mp):
    """See techmanual p.48 for calculation"""
    return math.ceil(walking_mp * 1.5)


def get_total_jumpjet_tonnage(mech_tonnage, jumping_mp):
    jumpjet_weight = 0
    if mech_tonnage >= 10 and mech_tonnage <= 55:
        jumpjet_weight = 0.5
    elif mech_tonnage >= 10 and mech_tonnage <= 55:
        jumpjet_weight = 1
    elif mech_tonnage >= 90 and mech_tonnage <= 100:
        jumpjet_weight = 2
    else: 
        print("something went wrong while calculating total_jumpjet_tonnage")
    
    total_jumpjet_tonnage = jumping_mp * jumpjet_weight
    return total_jumpjet_tonnage


# Calculate total heat sinks
def calculate_total_heatsinks(custom_mech):
    # Extract mech tonnage and walking movement points
    mech_tonnage = int(custom_mech["mech_data"]["tonnage"])
    walking_mp = int(custom_mech["mech_data"]["movement_points"]["walking"])

    # Calculate engine rating and internal heat sinks
    engine_rating = get_engine_rating(mech_tonnage, walking_mp)
    internal_heatsinks = get_internal_heatsinks(engine_rating)

    # Add any additional heat sinks from the mech configuration
    additional_heatsinks = sum(custom_mech["heatsinks"]["heatsink_locations"].values())

    # Total heatsinks = internal + additional
    total_heatsinks = internal_heatsinks + additional_heatsinks

    # Print debug information for total heatsinks
    print("Engine Rating:", engine_rating)
    print("Internal Heat Sinks:", internal_heatsinks)
    print("Additional Heat Sinks:", additional_heatsinks)
    print("Total Heat Sinks:", total_heatsinks)

    return total_heatsinks
