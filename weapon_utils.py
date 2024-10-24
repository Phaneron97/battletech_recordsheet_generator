import csv
from collections import defaultdict

# Function to load weapon data from a CSV file
def load_weapon_data(csv_filename):
    weapon_data = {}
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Name']
            weapon_data[name] = {
                'min': str(row['min']),
                'sht': str(row['Sht']),
                'med': str(row['Med']),
                'lng': str(row['Lng']),
                'ht': str(row['Ht']),
                'tech_base': row['tech base'],
                'weapon_type': row['weapon type'],
                'ton': str(row['Ton'])
            }
    return weapon_data

# Function to extract weapon details for the mech
def extract_weapon_details(weapons, weapon_data):
    weapon_details = []
    
    # Define a mapping of mech locations to weapon locations
    location_mapping = {
        'head': 'HD',
        'left_torso': 'LT',
        'right_torso': 'RT',
        'left_arm': 'LA',
        'right_arm': 'RA'
    }

    for location, weapon_info in weapons.items():
        for weapon_name, quantity in weapon_info.items():
            print(weapon_name)
            # Get the corresponding weapon attributes from the weapon data
            if weapon_name in weapon_data:
                
                weapon_attributes = weapon_data[weapon_name]
                weapon_details.append({
                    'quantity': quantity,
                    'name': weapon_name,
                    'location': location_mapping.get(location, 'Unknown'),
                    'heat': weapon_attributes['ht'],
                    'damage': 1,  # Assuming damage is fixed at 1 for now
                    'min': weapon_attributes['min'],
                    'sht': weapon_attributes['sht'],
                    'med': weapon_attributes['med'],
                    'lng': weapon_attributes['lng'],
                })

    return weapon_details
