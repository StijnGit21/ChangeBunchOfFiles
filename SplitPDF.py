import os
from PyPDF2 import PdfReader, PdfWriter

# Constante voor het bestandspad
PDF_PATH = r"C:\Users\stijn\Documents\voorbeeld.pdf"  # Vervang dit met je eigen pad

def split_pdf(pdf_path):
    # Maak een map met de naam van het bestand (zonder extensie)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_dir = os.path.join(os.path.dirname(pdf_path), base_name)
    os.makedirs(output_dir, exist_ok=True)

    # Open de PDF
    with open(pdf_path, "rb") as file:
        pdf_reader = PdfReader(file)

        # Loop door elke pagina
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_num])

            # Sla de pagina op als een nieuwe PDF
            output_filename = os.path.join(output_dir, f"{page_num + 1}.pdf")
            with open(output_filename, "wb") as output_file:
                pdf_writer.write(output_file)

    print(f"PDF is opgesplitst en opgeslagen in: {output_dir}")

if __name__ == "__main__":
    split_pdf(PDF_PATH)