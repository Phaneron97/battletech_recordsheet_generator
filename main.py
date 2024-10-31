# main

from pdf_utils import create_filled_pdf
from layout_data import custom_pdf, custom_mech
from weapon_utils import load_weapon_data, extract_weapon_details

# Load weapon data from CSV
weapon_data = load_weapon_data('weapons.csv')

# Extract weapon details from custom_mech
weapon_details = extract_weapon_details(custom_mech["weapons"], weapon_data)

output_filled_pdf = "pdfs/filled_record_sheet.pdf"
template_pdf = "pdfs/blank_record_sheet.pdf"

# Pass weapon_details to create_filled_pdf
create_filled_pdf(custom_mech, custom_pdf, output_filled_pdf, template_pdf, weapon_details)
