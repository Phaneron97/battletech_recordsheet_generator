import csv
import re

# Define the input and output filenames
input_filename = 'weapons_2.txt'
output_filename = 'weapons_2.csv'

# Define the columns as per the provided example
columns = [
    'Weapon/Item', 'Heat', 'Damage', 'Range', 'Ammo', 'WT', 'M', 
    'P', 'CV', 'SV', 'F', 'SC', 'DS', 'TechRating', 'PageRef'
]

# Function to process the text file and create a CSV
def convert_text_to_csv(input_file, output_file, columns):
    with open(input_file, 'r') as infile:
        # Read the file lines
        lines = infile.readlines()
        
    # Prepare the output data
    output_data = []
    
    # Add the header to output data only once
    output_data.append(columns)

    # Regex pattern to match the expected row format
    # This pattern captures the entire row without splitting inappropriately
    pattern = r'^(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)(\s*|\s+\d*)$'

    for line in lines:
        # Remove leading and trailing whitespace
        line = line.strip()
        
        # Match the line against the pattern
        match = re.match(pattern, line)
        if match:
            # If matched, extract the groups and append them to the output data
            output_data.append([group.strip() for group in match.groups() if group])
        else:
            print(f"Line didn't match the expected format: {line}")

    # Write the output data to CSV
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(output_data)

# Call the function to convert the text file to a CSV file
convert_text_to_csv(input_filename, output_filename, columns)

print(f'Data has been converted and saved to {output_filename}.')
