import pandas as pd

# Path to the input CSV file
input_csv = 'weapons.csv'

# Path to the output CSV file
output_csv = 'extracted_weapons.csv'

# Columns to extract
columns_to_extract = [
    'tech base', 
    'weapon type', 
    'Ton', 
    'Name', 
    'min', 
    'Sht', 
    'Med', 
    'Lng', 
    'Ht']

# Read the CSV file
df = pd.read_csv(input_csv)

# Extract the required columns
extracted_df = df[columns_to_extract]

extracted_df['Name'] = extracted_df['Name'].str.replace(' ', '_') # replace space with _
extracted_df['Name'] = extracted_df['Name'].str.replace('/', '') # replace / with nothing

# Save the extracted columns to a new CSV file
extracted_df.to_csv(output_csv, index=False)

print(f"Extracted columns with updated 'Name' column saved to {output_csv}")
