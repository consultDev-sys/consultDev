from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io 
import random
import string
from reportlab.lib.units import inch
from datetime import datetime
from quotation.constants import METADATA_PAGES
import textwrap
import requests

from reportlab.lib.utils import ImageReader
from io import BytesIO

class CreatePdf():

    def generate_random_metadata(self):
        # Generate random metadata for a page
        lines = []
        for i in range(30):  # Assuming 30 lines per page for simplicity
            line = ''.join(random.choices(string.ascii_letters + string.digits, k=60))
            lines.append(line)
        return lines

    def generate_pdf(self, customer, quotation, logo=1):
        # Create a byte stream buffer
        buffer = io.BytesIO()
        # Create a canvas object using the buffer as the file-like object
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle("Business License Report")

        # Define some basic settings for the PDF
        width, height = letter
        pdf.setFont("Helvetica", 12)
        line_height = 20
        left_margin = 1 * inch
        right_margin = width - 1 * inch
        top_margin = height - 1 * inch
        bottom_margin = 1 * inch

        for page in range(1, 7):
            y = top_margin  # Start from the top of the page

            if page == 1:
                # Store the initial y position for logo alignment
                initial_y = y

                # Add the customer's name, email, phone number, and date as shown in the image
                pdf.setFont("Helvetica-Bold", 24)
                pdf.setFillColorRGB(0.8, 0.0, 0.0)  # Set text color to match the red in the image
                pdf.drawString(left_margin, y, customer.first_name)
                y -= 25
                pdf.setFont("Helvetica-Bold", 24)
                pdf.setFillColorRGB(0.8, 0.0, 0.0)  # Set text color to match the red in the image
                pdf.drawString(left_margin, y, customer.last_name)
                y -= 40
                pdf.setFont("Helvetica", 12)
                pdf.setFillColorRGB(0, 0, 0)  # Set text color back to black
                pdf.drawString(left_margin, y, customer.email)
                y -= line_height
                pdf.drawString(left_margin, y, customer.phone_number)
                y -= line_height
                pdf.drawString(left_margin, y, datetime.today().strftime('%d/%b/%Y'))

                # Add the logo to the right side of the page
                if logo:
                    try:
                        # Download the image from S3
                        response = requests.get("https://emirateslaunchlogobucket.s3.amazonaws.com/1/Logotest.png")
                        img = ImageReader(BytesIO(response.content))

                        # Get the image dimensions
                        img_width, img_height = img.getSize()

                        # Calculate the aspect ratio
                        aspect = img_height / float(img_width)

                        # Set a maximum width for the logo (e.g., 2 inches)
                        max_width = 2 * inch
                        display_width = min(max_width, img_width)
                        display_height = display_width * aspect

                        # Calculate the position (right-aligned, top aligned with first name)
                        img_x = right_margin - display_width
                        img_y = initial_y - display_height  # Align top of logo with top of first name

                        # Draw the image
                        pdf.drawImage(img, img_x, img_y, width=display_width, height=display_height)
                    except Exception as e:
                        print(f"Error adding logo: {e}")

                y -= line_height * 2

            elif page == 2:
                # Add the freezone description on the second page
                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(left_margin, y, "Freezone Description")
                y -= line_height * 1.5
                pdf.setFont("Helvetica", 12)
                
                freezone_description = quotation['freezone_description']
                lines = freezone_description.split('\n')
                for line in lines:
                    wrapped_text = textwrap.fill(line, width=95)
                    for wrapped_line in wrapped_text.split('\n'):
                        pdf.drawString(left_margin, y, wrapped_line)
                        y -= line_height
                        if y < bottom_margin:
                            pdf.showPage()
                            pdf.setFont("Helvetica", 12)
                            y = top_margin

            elif page == 3:
                # Add content from the quotation dictionary
                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(left_margin, y, "Quotation Details")
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
                    pdf.drawString(left_margin, y, f"{label}:")
                    pdf.drawString(left_margin + 200, y, str(value))
                    y -= line_height * 1.5
            elif page == 4:
                # Add the allowed packages on the fourth page
                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(left_margin, y, "Allowed Packages")
                y -= line_height * 1.5
                pdf.setFont("Helvetica", 12)
                
                allowed_packages = quotation['allowed_packages']
                lines = allowed_packages.split('\n')
                for line in lines:
                    wrapped_text = textwrap.fill(line, width=95)
                    for wrapped_line in wrapped_text.split('\n'):
                        pdf.drawString(left_margin, y, wrapped_line)
                        y -= line_height
                        if y < bottom_margin:
                            pdf.showPage()
                            pdf.setFont("Helvetica", 12)
                            y = top_margin

            elif page == 5:
                # Add the allowed packages on the fourth page
                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(left_margin, y, "Visa and Compliance details")
                y -= line_height * 1.5
                pdf.setFont("Helvetica", 12)
                
                allowed_packages = quotation['compliance_details']
                lines = allowed_packages.split('\n')
                for line in lines:
                    wrapped_text = textwrap.fill(line, width=95)
                    for wrapped_line in wrapped_text.split('\n'):
                        pdf.drawString(left_margin, y, wrapped_line)
                        y -= line_height
                        if y < bottom_margin:
                            pdf.showPage()
                            pdf.setFont("Helvetica", 12)
                            y = top_margin
            else:
                # Add realistic metadata
                metadata = METADATA_PAGES[(page - 1) % len(METADATA_PAGES)]
                for line in metadata:
                    if y < bottom_margin:  # Move to next page if no more space
                        break
                    pdf.drawString(left_margin, y, line)
                    y -= line_height

            # Finalize the page and move to the next
            pdf.showPage()

        # Finalize the PDF
        pdf.save()

        # Move the buffer cursor to the beginning of the stream
        buffer.seek(0)
        return buffer