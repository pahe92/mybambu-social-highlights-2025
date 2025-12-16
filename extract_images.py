#!/usr/bin/env python3
"""
Extract post images from October 2025 report PDF
Saves images to the images/ directory for use in the HTML report
"""

import fitz  # PyMuPDF
import os

def extract_images_from_pdf(pdf_path, output_dir):
    """Extract images from specific pages of the PDF"""

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open PDF
    doc = fitz.open(pdf_path)

    # Define pages and image names
    image_extractions = [
        # Instagram posts (page 10 - index 9)
        (9, "instagram-greenacres-event.jpg"),
        (9, "instagram-tips-agregar-dinero.jpg"),
        (6, "instagram-reels.jpg"),  # Page 7 for videos

        # Facebook posts (page 14 - index 13)
        (13, "facebook-cashback.jpg"),
        (13, "facebook-apoyo-lejos.jpg"),
        (13, "facebook-tips.jpg"),

        # TikTok posts (pages 18-19 - index 17-18)
        (17, "tiktok-aprende-ingles.jpg"),
        (17, "tiktok-emprender.jpg"),
        (18, "tiktok-inmigrante.jpg"),

        # YouTube posts (page 22 - index 21)
        (21, "youtube-herencia-hispana.jpg"),
        (21, "youtube-pov.jpg"),
        (21, "youtube-emigrar.jpg"),
    ]

    extracted_count = 0

    for page_num, filename in image_extractions:
        try:
            page = doc[page_num]

            # Get images from page
            image_list = page.get_images(full=True)

            if image_list:
                # Take the first/largest image from each page
                xref = image_list[0][0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                # Save image
                output_path = os.path.join(output_dir, filename)
                with open(output_path, "wb") as img_file:
                    img_file.write(image_bytes)

                print(f"✓ Extracted: {filename}")
                extracted_count += 1
            else:
                # Take screenshot of page as fallback
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for quality
                output_path = os.path.join(output_dir, filename)
                pix.save(output_path)
                print(f"✓ Screenshot: {filename}")
                extracted_count += 1

        except Exception as e:
            print(f"✗ Error extracting {filename}: {e}")

    doc.close()
    print(f"\n✓ Extracted {extracted_count} images to {output_dir}/")

if __name__ == "__main__":
    pdf_path = "/Users/paulahernandez/Downloads/Reporte Mensual Octubre (1).pdf"
    output_dir = "/Users/paulahernandez/mybambu-social-highlights-2025/images"

    print("Extracting post images from October 2025 report...")
    extract_images_from_pdf(pdf_path, output_dir)
    print("\nDone! Images ready for HTML report.")
