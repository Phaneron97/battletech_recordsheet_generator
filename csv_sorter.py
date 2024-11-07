import csv

def sort_csv_by_columns(input_csv, output_csv):
    # Read the CSV file and store rows in a list
    with open(input_csv, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

        # Sort rows by 'Techbase', 'Weapon/Item', and 'BV'
        rows_sorted = sorted(rows, key=lambda x: (x['Techbase'], x['Weapon/Item']))

        # Write the sorted data to the output CSV
        with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows_sorted)

    print(f"CSV sorted by Techbase, Weapon/Item, and BV. Output saved to {output_csv}")

# Usage
input_csv = "merged_output.csv"  # Replace with your input file path
output_csv = "sorted_merged_output.csv"  # Specify output file path
sort_csv_by_columns(input_csv, output_csv)
