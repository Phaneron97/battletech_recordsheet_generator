import csv
import re

# Function to load weapon data from a new CSV file format
def load_weapon_data(csv_filename):
    """Loads weapon data from a new CSV file into a dictionary for quick lookup."""
    weapon_data = {}
    
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Strip whitespace from headers and rename keys to avoid lookup issues
        # headers = [header.strip() for header in reader.fieldnames]
        # print("CSV Headers (stripped):", headers)  # Debugging line to check headers

        for row in reader:
            # Strip whitespace from each key-value pair in the row
            row = {key.strip(): value.strip() for key, value in row.items()}
            # print("Row (stripped):", row)  # Debugging line to check each row

            # Normalize the name for consistent lookup
            name = row['Weapon/Item'].lower().replace(' ', '_')
            
            # Extract data while handling fields with additional formatting
            heat_match = re.search(r'\d+', row['Heat'])
            heat = heat_match.group() if heat_match else '0'  # Set to '0' if no match found
            
            # Extract damage excluding the part in parentheses
            # damage_match = re.search(r'^\d+', row['Damage'])
            damage = re.sub(r'\s*\(.*\)$', '', row['Damage']).strip()
            # damage = damage_match.group() if damage_match else '0'

            # Parse ranges using helper function
            min_range, sht_range, med_range, lng_range = parse_range(row['Range'])

            # Map data to match the structure expected by existing code
            weapon_data[name] = {
                'tech_base': row['Techbase'],
                'weapon_type': row.get('Weapon/Item', ''),
                'ton': row.get('WT', '0'),  # 'WT' is equivalent to 'Ton' in previous format
                'ht': heat,
                'dmg': damage,
                'min': min_range,
                'sht': sht_range,
                'med': med_range,
                'lng': lng_range,
                'slots': row.get('M', '0')  # 'P' is assumed as equivalent to 'Slots'
            }
            # print("weapon", weapon_data[name])
    return weapon_data

# Helper function to parse range values in the format "min/sht/med/lng"
def parse_range(range_str):
    """Parses the range string into min, short, medium, and long ranges."""
    ranges = re.findall(r'\d+', range_str)  # Extract all numeric values in the range
    min_range = ranges[0] if len(ranges) > 0 else '0'
    sht_range = ranges[1] if len(ranges) > 1 else '0'
    med_range = ranges[2] if len(ranges) > 2 else '0'
    lng_range = ranges[3] if len(ranges) > 3 else '0'

    return min_range, sht_range, med_range, lng_range

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
            normalized_name = weapon_name.lower()
            if normalized_name in weapon_data:
                weapon_attributes = weapon_data[normalized_name]
                # Add formatted weapon detail to the list
                weapon_details.append(format_weapon_detail(normalized_name, quantity, location, weapon_attributes))
            else:
                print(f"Warning: {weapon_name} not found in weapon data.")
                
    print("weapon details:", weapon_details)
    return weapon_details
