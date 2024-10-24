import pandas as pd

# Load the weapons CSV file into a DataFrame
weapons_df = pd.read_csv('weapons.csv')

# Convert the 'Slots' column to integers, replacing NaN with 0
weapons_df['Slots'] = weapons_df['Slots'].astype(float).fillna(0).astype(int)

# Remove duplicate rows based on the 'Name' column
# We keep the first occurrence, and only consider the 'Dmg' and 'Slots' columns for duplicates
# This means that if there are duplicates, the one with non-null 'Dmg' and 'Slots' values will be prioritized
weapons_df['Dmg'] = weapons_df['Dmg'].fillna(0)  # Fill NaN in 'Dmg' with 0 for comparison
weapons_df['Slots'] = weapons_df['Slots'].fillna(0)  # Fill NaN in 'Slots' with 0 for comparison

# Create a mask to keep only the rows where Dmg or Slots are not NaN
mask = weapons_df['Dmg'].ne(0) | weapons_df['Slots'].ne(0)

# Use the mask to filter the DataFrame before dropping duplicates
filtered_df = weapons_df[mask].drop_duplicates(subset='Name', keep='first')

# Combine filtered duplicates with the rest of the DataFrame
final_df = pd.concat([filtered_df, weapons_df[~mask]]).drop_duplicates()

# Sort the DataFrame by 'tech base', 'weapon type', and 'Name'
final_df = final_df.sort_values(by=['tech base', 'weapon type', 'Name'])

# Sort the DataFrame by 'tech base', 'weapon type', and 'Name'
sorted_weapons_df = final_df.sort_values(by=['tech base', 'weapon type', 'Name'])

# Save the sorted DataFrame to a new CSV file
sorted_weapons_df.to_csv('sorted_cleaned_weapons.csv', index=False)

print("Duplicates removed and data saved successfully.")
