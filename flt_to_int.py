import pandas as pd

# Load the weapons CSV file into a DataFrame
weapons_df = pd.read_csv('weapons.csv')

# Convert the 'Dmg' column from float to integer
weapons_df['Dmg'] = weapons_df['Dmg'].astype(int)

# Save the updated DataFrame to a new CSV file
weapons_df.to_csv('updated_weapons.csv', index=False)

print("Dmg column converted to integers and saved successfully.")
