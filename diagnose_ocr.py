from pathlib import Path
import json

ocr_dir = Path("outputs/ocr")
extracted_dir = Path("outputs/extracted")

print("OCR files:")
for path in sorted(ocr_dir.glob("*.json")):
    print(" -", path.name)

print("\nOCR text check:")
for path in sorted(ocr_dir.glob("*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))

    print(f"\n{path.name}")
    for item in data:
        text = item.get("ocr_text", "")
        print(
            f"  Page {item.get('page')}: "
            f"{len(text.strip())} OCR characters"
        )
        print("  Preview:", repr(text[:250]))

print("\nMatching extracted files:")
for path in sorted(extracted_dir.glob("*.json")):
    expected_ocr = ocr_dir / f"{path.stem}_ocr.json"
    print(path.name, "->", "FOUND" if expected_ocr.exists() else "NOT FOUND")