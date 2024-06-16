from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io 
import random
import string

from quotation.constants import METADATA_PAGES
class CreatePdf():

    def generate_random_metadata(self):
        # Generate random metadata for a page
        lines = []
        for i in range(30):  # Assuming 30 lines per page for simplicity
            line = ''.join(random.choices(string.ascii_letters + string.digits, k=60))
            lines.append(line)
        return lines

    def generate_pdf(self, quotation):
        # Create a byte stream buffer
        buffer = io.BytesIO()
        # Create a canvas object using the buffer as the file-like object
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle("Business License Report")

        # Define some basic settings for the PDF
        width, height = letter
        pdf.setFont("Helvetica", 12)
        line_height = 20
        logo_path = "/home/consultant/consultDev/assets/random.svg"
        for page in range(1, 7):
            y = height - 40  # Start from the top of the page

            if page == 1:
                # Add the logo on the top left of the first page
                pdf.drawImage(logo_path, 30, height - 100, width=100, height=50)  # Adjust width and height as needed
                y -= 80  # Adjust the starting position to avoid overlapping with the logo

                # Add a title and introductory paragraph on the first page
                pdf.setFont("Helvetica-Bold", 16)
                pdf.drawString(150, height - 60, "Business License Report")
                pdf.setFont("Helvetica", 12)
                pdf.drawString(30, y, "This report provides detailed information about the business license costs and associated services.")
                y -= line_height
                pdf.drawString(30, y, "It includes a breakdown of costs for license, establishment, e-channel, residence visa, medical, and more.")
                y -= line_height * 2

            if page == 3:
                # Add content from the quotation dictionary
                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(30, y, "Quotation Details")
                y -= line_height * 1.5
                pdf.setFont("Helvetica", 12)
                quotation_items = [
                    ("License Cost", quotation['license_cost']),
                    ("Establishment", quotation['establishment']),
                    ("E Channel", quotation['e_channel']),
                    ("Residence Visa", quotation['residence_visa']),
                    ("Medical", quotation['medical']),
                    ("Total Amount", quotation['total_amount']),
                    ("Emirate", quotation['emirate']),
                    ("Freezone", quotation['freezone']),
                    ("Business Activity", quotation['business_activity']),
                    ("Visa Packages", quotation['visa_packages'])
                ]
                for label, value in quotation_items:
                    pdf.drawString(30, y, f"{label}:")
                    pdf.drawString(200, y, str(value))
                    y -= line_height * 1.5
            else:
                # Add realistic metadata
                metadata = METADATA_PAGES[(page - 1) % len(METADATA_PAGES)]
                for line in metadata:
                    if y < 40:  # Move to next page if no more space
                        break
                    pdf.drawString(30, y, line)
                    y -= line_height

            # Finalize the page and move to the next
            pdf.showPage()

        # Finalize the PDF
        pdf.save()

        # Move the buffer cursor to the beginning of the stream
        buffer.seek(0)
        return buffer