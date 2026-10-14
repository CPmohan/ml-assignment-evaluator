"""OCR PDF pages that have little or no extractable text.

This script leaves extracted JSON files untouched. It writes one OCR JSON file
per PDF in outputs/ocr, containing only pages selected for OCR.
"""

import json
import os
from pathlib import Path

import pymupdf


PDF_DIR = Path("data/assignments")
OUTPUT_DIR = Path("outputs/ocr")
TESSERACT_EXE = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
TESSDATA_DIR = Path(r"C:\Program Files\Tesseract-OCR\tessdata")
LANGUAGE = "eng"
MIN_CHARS = 100


def configure_tesseract() -> None:
    """Validate the local Tesseract installation for PyMuPDF OCR."""
    language_data = TESSDATA_DIR / f"{LANGUAGE}.traineddata"

    if not TESSERACT_EXE.is_file():
        raise RuntimeError(
            "Tesseract executable was not found at "
            f"{TESSERACT_EXE}. Install Tesseract for Windows, or update "
            "TESSERACT_EXE in this script."
        )

    if not language_data.is_file():
        raise RuntimeError(
            "English Tesseract language data was not found at "
            f"{language_data}. Install the English language data, or update "
            "TESSDATA_DIR in this script."
        )

    # PyMuPDF's OCR API reads this directory; it does not use pytesseract.
    os.environ["TESSDATA_PREFIX"] = str(TESSDATA_DIR)


def needs_ocr(text: str) -> bool:
    """Return True when extracted text has fewer than MIN_CHARS non-whitespace characters."""
    return len("".join(text.split())) < MIN_CHARS


def ocr_pdf(pdf_path: Path) -> list[dict]:
    """OCR qualifying pages in one PDF and return their result records."""
    page_results: list[dict] = []

    with pymupdf.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            extracted_text = page.get_text("text")

            if not needs_ocr(extracted_text):
                continue

            original_text = extracted_text.strip()
            print(f"OCR: {pdf_path.name} | page {page_number}")

            result = {
                "filename": pdf_path.name,
                "page": page_number,
                "original_text": original_text,
            }

            try:
                ocr_text_page = page.get_textpage_ocr(
                    language=LANGUAGE,
                    dpi=300,
                    full=True,
                )
                result["ocr_text"] = page.get_text(
                    "text", textpage=ocr_text_page
                ).strip()
            except Exception as error:
                result["ocr_error"] = str(error)

            page_results.append(result)

    return page_results


def main() -> None:
    configure_tesseract()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in: {PDF_DIR.resolve()}")
        return

    for pdf_path in pdf_files:
        page_results = ocr_pdf(pdf_path)
        if not page_results:
            continue

        output_path = OUTPUT_DIR / f"{pdf_path.stem}_ocr.json"
        output_path.write_text(
            json.dumps(page_results, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Saved: {output_path}")

    print("OCR pass completed.")


if __name__ == "__main__":
    main()
