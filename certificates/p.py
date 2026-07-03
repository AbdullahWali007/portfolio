#Script to Convert .pdf Certificates into images in batches.
#You can use this script if you have multiple pdf certificates, it saves time
import os
import fitz  # PyMuPDF
from PIL import Image


def convert_pdf(pdf_path, output_format):
    """
    Convert all pages of a PDF to images.
    """

    folder = os.path.dirname(pdf_path)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f" Could not open {pdf_path}")
        print(e)
        return

    total_pages = len(doc)

    for page_num in range(total_pages):
        page = doc.load_page(page_num)

        # Higher resolution (2x zoom)
        matrix = fitz.Matrix(2, 2)

        pix = page.get_pixmap(matrix=matrix)

        mode = "RGBA" if pix.alpha else "RGB"

        image = Image.frombytes(
            mode,
            [pix.width, pix.height],
            pix.samples
        )

        # Keep original filename
        if total_pages == 1:
            output_name = f"{pdf_name}.{output_format.lower()}"
        else:
            output_name = f"{pdf_name}_page_{page_num + 1}.{output_format.lower()}"

        output_path = os.path.join(folder, output_name)

        if output_format.lower() == "webp":
            image.save(output_path, "WEBP", quality=100)
        else:
            image.save(output_path, "PNG")

        print(f" Saved: {output_name}")

    doc.close()


def main():
    folder = input("Enter the folder path containing PDFs: ").strip()

    if not os.path.isdir(folder):
        print(" Invalid folder path.")
        return

    print("\nChoose output format:")
    print("1. PNG")
    print("2. WEBP")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        output_format = "png"
    elif choice == "2":
        output_format = "webp"
    else:
        print(" Invalid choice.")
        return

    pdf_found = False

    for file in os.listdir(folder):

        # Ignore everything except PDFs
        if not file.lower().endswith(".pdf"):
            continue

        pdf_found = True

        pdf_path = os.path.join(folder, file)

        print(f"\nProcessing: {file}")
        convert_pdf(pdf_path, output_format)

    if not pdf_found:
        print("\n⚠ No PDF files found.")

    print("\n Done!")


if __name__ == "__main__":
    main()
