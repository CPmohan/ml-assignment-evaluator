from pathlib import Path
import json
import fitz  # PyMuPDF

PDF_DIR = Path("data/assignments")
OUT_DIR = Path("outputs/extracted")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_pdf(pdf_path: Path) -> dict:
    pages = []

    with fitz.open(pdf_path) as doc:
        for page_number, page in enumerate(doc, start=1):
            pages.append({
                "page": page_number,
                "text": page.get_text("text").strip()
            })

    full_text = "\n\n".join(p["text"] for p in pages)

    return {
        "filename": pdf_path.name,
        "page_count": len(pages),
        "text": full_text,
        "pages": pages
    }

def main():
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDFs found in {PDF_DIR.resolve()}")
        return

    for pdf_path in pdf_files:
        result = extract_pdf(pdf_path)
        output_path = OUT_DIR / f"{pdf_path.stem}.json"
        output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(
            f"{pdf_path.name}: {result['page_count']} pages, "
            f"{len(result['text'])} characters"
        )

    print(f"\nProcessed {len(pdf_files)} PDFs.")

if __name__ == "__main__":
    main()