custom_pdf = {
    "mech_data": {
        "type": {
            "x": 70.0,
            "y": 147,
            "font": "EurostileBold",
            "size": 10,
            "margin": 1
        },
        "movement_points": {
            "walking": {
                "x": 100,
                "y": 171,
                "font": "Eurostile",
                "size": 10,
                "margin": 1
            },
            "running": {
                "x": 100,
                "y": 182,
                "font": "Eurostile",
                "size": 10,
                "margin": 1
            },
            "jumping": {
                "x": 100,
                "y": 192,
                "font": "Eurostile",
                "size": 10,
                "margin": 1
            }
        },        
        "tonnage": {
            "x": 195,
            "y": 160,
            "font": "Eurostile",
            "size": 10,
            "margin": 1
        },
        "weapons_and_equipment_inv_text": {
            "x": 42,
            "y": 557,
            "width": 199,
            "height": 139,
            "margin": 1
        },
        "weapons_and_equipment_inv_empty_placeholder": {
            "x": 42,
            "y": 226,
            "width": 199,
            "height": 139,
            "margin": 1
        },
    },    
    "tech_base_checkmark": {
        "IS": {"x": 221, "y": 192},  # Adjust these coordinates as needed
        "C": {"x": 221, "y": 182}    # Adjust these coordinates as needed
    },    
    "mech_image": {
        "x": 249,
        "y": 198,
        "width": 145,
        "height": 202,
        "margin": 1
    },    
    "armor_diagram": {
        "x": 396,
        "y": 78,
        "width": 180,
        "height": 317,
        "margin": 1,
        "head": {
            "x": 475,
            "y": 96,
            "width": 20,
            "height": 20,
            "rotation": 0,
            "margin": 1
        },
        "center_torso": {
            "x": 475,
            "y": 130,
            "width": 20,
            "height": 80,
            "rotation": 0,
            "margin": 1
        },
        "left_torso": {
            "x": 440,
            "y": 115,
            "width": 20,
            "height": 75,
            "rotation": 3,
            "margin": 1
        },
        "right_torso": {
            "x": 510,
            "y": 115,
            "width": 20,
            "height": 75,
            "rotation": -3,
            "margin": 1
        },
        "left_arm": {
            "x": 415,
            "y": 110,
            "width": 15,
            "height": 80,
            "rotation": -6,  
            "margin": 1
        },
        "right_arm": {
            "x": 541,
            "y": 110,
            "width": 15,
            "height": 80,
            "rotation": 6,  
            "margin": 1
        },
        "left_leg": {
            "x": 445,
            "y": 205,
            "width": 18,
            "height": 100,
            "rotation": -12,  
            "margin": 1
        },
        "right_leg": {
            "x": 505,
            "y": 205,
            "width": 18,
            "height": 100,
            "rotation": 12,  
            "margin": 1
        },
        "rear_center": {
            "x": 475,
            "y": 327,
            "width": 20,
            "height": 59,
            "rotation": 0,  
            "margin": 1
        },
        "rear_left": {
            "x": 442,
            "y": 337,
            "width": 20,
            "height": 30,
            "rotation": 0,  
            "margin": 1
        },
        "rear_right": {
            "x": 508,
            "y": 337,
            "width": 20,
            "height": 30,
            "rotation": 0,  
            "margin": 1
        }
    },
    "structure_diagram": {
        "x": 394,
        "y": 413,
        "width": 160,
        "height": 172,
        "margin": 1,
        "head": {
            "x": 467,
            "y": 425,
            "width": 12,
            "height": 12,
            "rotation": 0,
            "margin": 1
        },
        "center_torso": {
            "x": 466,
            "y": 445,
            "width": 14,
            "height": 50,
            "rotation": 0,
            "margin": 1
        },
        "left_torso": {
            "x": 440,
            "y": 430,
            "width": 14,
            "height": 45,
            "rotation": 3,
            "margin": 1
        },
        "right_torso": {
            "x": 510,
            "y": 450,
            "width": 20,
            "height": 75,
            "rotation": -3,
            "margin": 1
        },
        "left_arm": {
            "x": 415,
            "y": 450,
            "width": 15,
            "height": 80,
            "rotation": -6,  
            "margin": 1
        },
        "right_arm": {
            "x": 541,
            "y": 450,
            "width": 15,
            "height": 80,
            "rotation": 6,  
            "margin": 1
        },
        "left_leg": {
            "x": 445,
            "y": 600,
            "width": 18,
            "height": 100,
            "rotation": -12,  
            "margin": 1
        },
        "right_leg": {
            "x": 505,
            "y": 600,
            "width": 18,
            "height": 100,
            "rotation": 12,  
            "margin": 1
        }
    },
    "heat_data": {
        "empty_placeholder": {
            "x": 1,
            "y": 1,
            "width": 100,
            "height": 100,
            "rotation": 0,  
            "margin": 1
        },
        "heat_data_diagram": {
            "x": 50,
            "y": 50,
            "width": 30,
            "height": 100, 
            "rotation": 0,  
            "margin": 10
        },
    }
}

custom_mech = {
    "mech_data": {
        "type": "Atlas",
        "tonnage": "85",
        "tech_base": "IS",
        "movement_points": {
            "walking": "4",
            "running": "6",
            "jumping": "0"
        },
        "arm_parts": {
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
            "Medium_Laser": 3
        },
        "right_torso": {
            "Medium_Laser": 3,
            "SRM_6": 1
        },
        "left_arm": {
            "PPC": 1
        },
        "right_arm": {
            "Machine_Gun": 2
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
            "Machine_gun": 1
        }
    }
}
