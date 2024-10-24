layout_info = {
    "type": {
        "x": 70.0,
        "y": 147,
        "font": "EurostileBold",
        "size": 10,
        "margin": 1
    },
    "walking": {
        "x": 90,
        "y": 171,
        "font": "Eurostile",
        "size": 10,
        "margin": 1
    },
    "running": {
        "x": 90,
        "y": 182,
        "font": "Eurostile",
        "size": 10,
        "margin": 1
    },
    "jumping": {
        "x": 90,
        "y": 192,
        "font": "Eurostile",
        "size": 10,
        "margin": 1
    },
    "tonnage": {
        "x": 187,
        "y": 160,
        "font": "Eurostile",
        "size": 10,
        "margin": 1
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
            "rotation": -6,  # Example rotation in degrees
            "margin": 1
        },
        "right_arm": {
            "x": 541,
            "y": 110,
            "width": 15,
            "height": 80,
            "rotation": 6,  # Example rotation in degrees
            "margin": 1
        },
        "left_leg": {
            "x": 445,
            "y": 205,
            "width": 18,
            "height": 100,
            "rotation": -12,  # Example rotation in degrees
            "margin": 1
        },
        "right_leg": {
            "x": 505,
            "y": 205,
            "width": 18,
            "height": 100,
            "rotation": 12,  # Example rotation in degrees
            "margin": 1
        },
        "rear_center": {
            "x": 475,
            "y": 327,
            "width": 20,
            "height": 59,
            "rotation": 0,  # Example rotation in degrees
            "margin": 1
        },
        "rear_left": {
            "x": 442,
            "y": 337,
            "width": 20,
            "height": 30,
            "rotation": 0,  # Example rotation in degrees
            "margin": 1
        },
        "rear_right": {
            "x": 508,
            "y": 337,
            "width": 20,
            "height": 30,
            "rotation": 0,  # Example rotation in degrees
            "margin": 1
        }
    }
}

mech_data = {
    "type": "BattleMaster BLR-1G",
    "tonnage": "85",
    "walking": "3",
    "running": "5",
    "jumping": "0",
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
    "weapons": {
        "head": {
            "Small_Laser": 1
        },
        "left_torso": {
            "PPC": 1,
            "Medium_laser": 1
        },
        "right_torso": {
            "LRM_5": 1
        },
        "left_arm": {
            "Medium_laser": 2
        }
    }
}
