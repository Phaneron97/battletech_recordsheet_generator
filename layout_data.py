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
        "x": 396,
        "y": 278,
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
    }
}

custom_mech = {
    "mech_data": {
        "type": "BattleMaster BLR-1G",
        "tonnage": "85",
        "tech_base": "IS",
        "movement_points": {
            "walking": "3",
            "running": "5",
            "jumping": "0"
        },
        "arm_parts": {
            "lower_arm_actuator": True,
            "hand_actuator": True
        }
    },    
    "armor_points": {
        "head": 9,
        "center_torso": 9,
        "left_torso": 8,
        "right_torso": 35,
        "left_arm": 10,
        "right_arm": 10,
        "left_leg": 10,
        "right_leg": 10,
        "rear_center": 5,
        "rear_left": 4,
        "rear_right": 4
    },
    "structure_points": {
        "head": 3,
        "center_torso": 4,
        "left_torso": 5,
        "right_torso": 6,
        "left_arm": 7,
        "right_arm": 8,
        "left_leg": 9,
        "right_leg": 10,
        "rear_center": 11,
        "rear_left": 2,
        "rear_right": 13
    },
    "weapons": {
        "head": {
            "Small_Laser": 1
        },
        "left_torso": {
            "PPC": 1,
            "Medium_laser": 1,
            "Large_laser": 1,
            "ac10": 1,
            "ac5": 1,
            "lrm5": 1,
            "lrm10": 1,
            "lrm15": 1,
            "lrm20": 1
        },
        "right_torso": {
            "LRM_5": 1
        },
        "left_arm": {
            "Medium_laser": 2
        }
    },
    "heatsinks": {
        "heatsink_type": "single",
        "heatsink_locations": {
            "head": 1,
            "left_torso": 1,
            "right_torso": 3,
            "right_arm": 2,
            "left_arm": 2,
            "right_leg": 2,
            "left_leg": 2
        }
    }
}
