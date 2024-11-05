# Function to remove spaces after each comma in a CSV file
def remove_spaces_after_commas(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Replace ", " with "," to remove space after each comma
            cleaned_line = line.replace(', ', ',')
            outfile.write(cleaned_line)

# Specify the input and output file names
input_filename = 'weapons_and_ammo.csv'
output_filename = 'weapons_and_ammo_cleaned.csv'

# Call the function
remove_spaces_after_commas(input_filename, output_filename)
print(f"Spaces after commas have been removed. Check '{output_filename}'.")
