
import json
from pathlib import Path

# Update this filename if you want to grade a different submission.
INPUT_FILE = Path("outputs/merged/AryaR_AM_En_P2GEO23002_Assignment1.json")
OUTPUT_FILE = Path("outputs/graded/arya_draft_grade.json")

# Provisional rubric based on the assignment instructions.
# Confirm the detailed subdivisions with your advisor.
RUBRIC = [
    {
        "id": "A",
        "criterion": "Section A dataset questions",
        "max_marks": 1,
        "note": "Award only if all required Section A questions are answered."
    },
    {
        "id": "B1",
        "criterion": "Scatter-plot analysis",
        "max_marks": 1,
        "note": "Look for scatter plots comparing X1-X4 with Y."
    },
    {
        "id": "B2",
        "criterion": "Predictor selection",
        "max_marks": 1,
        "note": "Look for a clearly identified best predictor."
    },
    {
        "id": "B3",
        "criterion": "Plot evidence",
        "max_marks": 1,
        "note": "Look for plots or readable screenshots supporting the choice."
    },
    {
        "id": "B4",
        "criterion": "Explanation of predictor choice",
        "max_marks": 1,
        "note": "Look for an explanation based on the plotted relationship."
    },
    {
        "id": "C",
        "criterion": "Number of samples",
        "max_marks": 1,
        "note": "Expected dataset size: 414 samples."
    },
    {
        "id": "D",
        "criterion": "Train/test split",
        "max_marks": 1,
        "note": "Look for the split ratio used."
    },
    {
        "id": "E1",
        "criterion": "MAE",
        "max_marks": 1,
        "note": "Look for MAE calculation or output."
    },
    {
        "id": "E2",
        "criterion": "MSE",
        "max_marks": 1,
        "note": "Look for MSE calculation or output."
    },
    {
        "id": "E3",
        "criterion": "MAPE",
        "max_marks": 1,
        "note": "Look for MAPE calculation or output."
    }
]


def load_assignment(path):
    if not path.exists():
        raise FileNotFoundError(
            f"Could not find {path}. Check the filename and folder."
        )

    data = json.loads(path.read_text(encoding="utf-8"))

    # Support either a list of pages or a dictionary containing pages.
    if isinstance(data, dict):
        pages = data.get("pages", [])
    elif isinstance(data, list):
        pages = data
    else:
        raise ValueError("Unexpected JSON structure.")

    texts = []
    for page in pages:
        if isinstance(page, dict):
            texts.append(str(page.get("text", "")))
        else:
            texts.append(str(page))

    return "\n".join(texts)


def main():
    text = load_assignment(INPUT_FILE)

    print("\n=== ASSIGNMENT TEXT PREVIEW ===")
    print(text[:2500] or "[No text extracted]")

    print("\n=== DRAFT GRADING ===")
    results = []
    total = 0

    for item in RUBRIC:
        print(f"\n{item['id']}. {item['criterion']}")
        print(f"Max marks: {item['max_marks']}")
        print(f"Rubric guidance: {item['note']}")
        print("Read the PDF and enter the mark for this criterion.")

        while True:
            try:
                mark = float(input("Awarded marks: "))
                if 0 <= mark <= item["max_marks"]:
                    break
                print("Enter a mark within the allowed range.")
            except ValueError:
                print("Please enter a number.")

        evidence = input("Evidence/page number (or reason for 0): ").strip()

        results.append({
            **item,
            "awarded_marks": mark,
            "evidence": evidence
        })
        total += mark

    output = {
        "assignment_file": INPUT_FILE.name,
        "evaluation_type": "manual rubric-based draft",
        "rubric_status": "provisional; advisor approval pending",
        "total_awarded": total,
        "total_possible": sum(x["max_marks"] for x in RUBRIC),
        "criteria": results
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"\nDraft score: {total}/10")
    print(f"Saved result to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()