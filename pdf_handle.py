from PyPDF2 import PdfMerger, PdfReader
from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas

def reorganize_pdf(original_file_path: str, output_file_path: str, pages_per_output_pdf: int) -> None:
    # Create a new PDF file to hold the merged pages
    output_pdf = PdfMerger()
    # Loop through all the output pdf files
    with open(original_file_path, 'rb') as file:
        reader = PdfReader(file)
        for i in range(0, len(reader.pages), pages_per_output_pdf):
            output_pdf_temp = PdfMerger()
            for j in range(i, i + pages_per_output_pdf):
                # Add the page to the output PDF
                if j < len(reader.pages):
                    output_pdf_temp.append(PdfReader(original_file_path), pages=(j, j+1))
            output_pdf_temp.write("output{}.pdf".format(i))
            output_pdf.append("output{}.pdf".format(i))
    # Save the merged pdf file
    output_pdf.write(output_file_path)

