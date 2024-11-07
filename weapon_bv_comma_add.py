# Define the expected number of columns
expected_columns = 4

# Open the CSV file and check for rows with missing columns
with open("formatted_weapon_data2.csv", "r", encoding="utf-8") as infile:
    for line_num, line in enumerate(infile, start=1):
        # Split by comma to check column count
        columns = line.strip().split(',')
        
        # Check if the row has the expected number of columns
        if len(columns) != expected_columns:
            print(f"Row {line_num} has {len(columns)} columns: {line.strip()}")
