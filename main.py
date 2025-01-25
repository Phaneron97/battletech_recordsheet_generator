# main

from pdf_utils import create_filled_pdf
from layout_data import custom_pdf
from weapon_utils import load_weapon_data, extract_weapon_details

# Load weapon data from CSV
weapon_data = load_weapon_data('weapons_and_ammo.csv')
# weapon_data.head()

custom_mech = {
    "mech_data": {
        "type": "Battlemaster",
        "tonnage": "85",
        "tech_base": "IS",
        "movement_points": {
            "walking": "4",
            "running": "6",
            "jumping": "0"
        },
        "left_arm_parts": {
            "lower_arm_actuator": True,
            "hand_actuator": True
        },
        "right_arm_parts": {
            "lower_arm_actuator": True,
            "hand_actuator": True
        }
    },    
    "armor_points": {
        "head": 9,
        "center_torso": 40,
        "left_torso": 28,
        "right_torso": 28,
        "left_arm": 24,
        "right_arm": 24,
        "left_leg": 26,
        "right_leg": 26,
        "rear_center": 11,
        "rear_left": 8,
        "rear_right": 8
    },
    "structure_points": {
        "head": 3,
        "center_torso": 27,
        "left_torso": 18,
        "right_torso": 18,
        "left_arm": 14,
        "right_arm": 14,
        "left_leg": 16,
        "right_leg": 16
    },
    "weapons": {
        "head": {
        },
        "left_torso": {
            "Medium Laser": 3
        },
        "right_torso": {
            "Medium Laser": 3,
            "SRM 6": 1
        },
        "left_arm": {
            "PPC": 1
        },
        "right_arm": {
            "Machine Gun": 2
        }
    },
    "heatsinks": {
        "heatsink_type": "single",
        "heatsink_locations": {
            "right_torso": 1,
            "right_leg": 2,
            "left_leg": 2
        }
    },
    "ammunition": {
        "left_torso": {
            "SRM": 2,
            "Machine gun": 1
        }
    }
}

# Extract weapon details from custom_mech
weapon_details = extract_weapon_details(custom_mech["weapons"], weapon_data)
print("weapon_details", weapon_details)

output_filled_pdf = "pdfs/filled_record_sheet.pdf"
template_pdf = "pdfs/blank_record_sheet.pdf"

# Pass weapon_details to create_filled_pdf
create_filled_pdf(custom_mech, custom_pdf, output_filled_pdf, template_pdf, weapon_details)