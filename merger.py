import pandas as pd

# List of new weapons to add
new_weapons_data = {
    "tech base": ["IS"] * 15,
    "weapon type": ["Balistic", "Balistic", "Balistic", "Missile", "Missile", "Missile", "Missile", "Missile", "Missile", "Missile", "Energy", "Energy", "Energy", "Energy", "Balistic"],
    "Ton": [12.0, 8.0, 6.0, 1.0, 2.0, 3.0, 2.0, 5.0, 7.0, 10.0, 1.0, 5.0, 0.5, 7.0, 0.5],
    "Name": ["AC10", "AC5", "AC2", "SRM_2", "SRM_4", "SRM_6", "LRM_5", "LRM_10", "LRM_15", "LRM_20", "Medium_Laser", "Large_Laser", "Small_Laser", "PPC", "Machine_Gun"],
    "min": [0, 3, 4, 0, 0, 0, 6, 6, 6, 6, 0, 0, 0, 3, 0],
    "Sht": [5, 6, 8, 3, 3, 3, 7, 7, 7, 7, 3, 5, 1, 6, 1],
    "Med": [10, 12, 16, 6, 6, 6, 14, 14, 14, 14, 6, 10, 2, 12, 2],
    "Lng": [15, 18, 24, 9, 9, 9, 21, 21, 21, 21, 9, 15, 3, 18, 3],
    "Ht": [3, 1, 1, 2, 3, 4, 2, 4, 5, 6, 3, 8, 3, 10, 0],
    "Dmg": [10, 5, 2, 2, 8, 12, 5, 10, 15, 20, 5, 8, 3, 10, 2],
    "Slots": [7, 4, 3, 1, 1, 2, 1, 2, 3, 5, 1, 2, 1, 3, 1]
}

# Convert to DataFrame
new_weapons_df = pd.DataFrame(new_weapons_data)

# Load the current weapons CSV (assuming it's already loaded as a DataFrame)
current_weapons_df = pd.read_csv('extracted_weapons.csv')

# Concatenate the new weapons with the current weapons
merged_weapons_df = pd.concat([current_weapons_df, new_weapons_df])

# Convert float columns to integers
columns_to_convert = ['Ton', 'min', 'Sht', 'Med', 'Lng', 'Ht', 'Dmg', 'Slots']
int_columns = ['Slots']
merged_weapons_df[int_columns] = merged_weapons_df[int_columns].astype(int)

# Remove duplicates based on the 'Name' column, keeping the first occurrence
merged_weapons_df = merged_weapons_df.drop_duplicates(subset='Name', keep='first')

# Save the merged DataFrame to a new CSV file
merged_weapons_df.to_csv('merged_weapons.csv', index=False)

print("Weapons merged and saved successfully.")
