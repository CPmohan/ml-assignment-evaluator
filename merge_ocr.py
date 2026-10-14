from pathlib import Path
import json

EXTRACTED_DIR = Path("outputs/extracted")
OCR_DIR = Path("outputs/ocr")
MERGED_DIR = Path("outputs/merged")

MERGED_DIR.mkdir(parents=True, exist_ok=True)

def main():
    for extracted_file in sorted(EXTRACTED_DIR.glob("*.json")):
        data = json.loads(extracted_file.read_text(encoding="utf-8"))

        # OCR file has the same filename stem plus "_ocr".
        ocr_file = OCR_DIR / f"{extracted_file.stem}_ocr.json"

        ocr_by_page = {}

        if ocr_file.exists():
            ocr_pages = json.loads(ocr_file.read_text(encoding="utf-8"))
            ocr_by_page = {
                item["page"]: item
                for item in ocr_pages
            }

        merged_pages = []

        for page in data.get("pages", []):
            page_number = page["page"]
            original_text = page.get("text", "")
            ocr_item = ocr_by_page.get(page_number)

            merged_text = original_text
            source = "text_layer"

            if ocr_item and ocr_item.get("ocr_text"):
                # Keep original text and append OCR text for review.
                merged_text = (
                    original_text
                    + "\n\n[OCR TEXT]\n"
                    + ocr_item["ocr_text"]
                )
                source = "text_layer+ocr"

            merged_pages.append({
                "page": page_number,
                "text": merged_text,
                "source": source
            })

        data["pages"] = merged_pages
        data["text"] = "\n\n".join(
            page["text"] for page in merged_pages
        )
        data["ocr_merged"] = True

        output_file = MERGED_DIR / extracted_file.name
        output_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        ocr_count = sum(
            1 for page in merged_pages
            if page["source"] == "text_layer+ocr"
        )

        print(
            f"{data['filename']} | "
            f"pages={len(merged_pages)} | "
            f"OCR pages merged={ocr_count}"
        )

    print(f"\nMerged files saved in: {MERGED_DIR.resolve()}")

if __name__ == "__main__":
    main()