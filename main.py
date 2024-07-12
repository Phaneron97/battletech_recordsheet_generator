from pdf_utils import create_filled_pdf
from layout_data import layout_info, mech_data

output_filled_pdf = "pdfs/test.pdf"
template_pdf = "pdfs/blank_record_sheet.pdf"

create_filled_pdf(mech_data, layout_info, output_filled_pdf, template_pdf)
