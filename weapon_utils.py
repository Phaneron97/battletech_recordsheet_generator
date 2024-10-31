import csv

# Function to load weapon data from a CSV file
def load_weapon_data(csv_filename):
    """Loads weapon data from a CSV file into a dictionary for quick lookup."""
    weapon_data = {}
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Normalize the name for consistent lookup
            name = row['Name'].lower().replace('_', '')
            weapon_data[name] = {
                'min': str(row['min']),
                'sht': str(row['Sht']),
                'med': str(row['Med']),
                'lng': str(row['Lng']),
                'ht': str(row['Ht']),
                'dmg': str(row['Dmg']),
                'slots': str(row['Slots']),
                'tech_base': row['tech base'],
                'weapon_type': row['weapon type'],
                'ton': str(row['Ton'])
            }
    return weapon_data

# Function to map mech locations to abbreviations
def map_location(location):
    """Maps mech component locations to abbreviated labels used in PDF layout."""
    location_mapping = {
        'head': 'HD',
        'left_torso': 'LT',
        'right_torso': 'RT',
        'left_arm': 'LA',
        'right_arm': 'RA'
    }
    return location_mapping.get(location, 'Unknown')

# Function to format a weapon's attributes into a dictionary entry for the PDF
def format_weapon_detail(weapon_name, quantity, location, weapon_attributes):
    """Formats weapon data for insertion into PDF layout, including location and quantity."""
    return {
        'quantity': quantity,
        'name': weapon_name,
        'location': map_location(location),
        'heat': weapon_attributes['ht'],
        'damage': weapon_attributes['dmg'],
        'min': weapon_attributes['min'],
        'sht': weapon_attributes['sht'],
        'med': weapon_attributes['med'],
        'lng': weapon_attributes['lng'],
        'slots': weapon_attributes['slots']
    }

# Function to extract weapon details for the mech
def extract_weapon_details(weapons, weapon_data):
    """Extracts and formats weapon details for each mech component from weapon data."""
    weapon_details = []

    for location, weapon_info in weapons.items():
        for weapon_name, quantity in weapon_info.items():
            # Lookup weapon attributes, ensuring name consistency with loaded data
            normalized_name = weapon_name.lower().replace('_', '')
            if normalized_name in weapon_data:
                weapon_attributes = weapon_data[normalized_name]
                # Add formatted weapon detail to the list
                weapon_details.append(format_weapon_detail(normalized_name, quantity, location, weapon_attributes))
            else:
                print(f"Warning: {weapon_name} not found in weapon data.")
                
    return weapon_details
