"""Calculate AI–human agreement only from supplied, verified score pairs."""

import json
from pathlib import Path

import csv
import math


ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "data" / "human_marks.csv"
OUTPUT = ROOT / "outputs" / "performance_analysis.json"
STATUS_OUTPUT = ROOT / "outputs" / "performance_analysis_status.json"
REQUIRED = {"assignment", "criterion_id", "human_score", "ai_score"}


def cohens_kappa(human_scores: list[float], ai_scores: list[float]) -> float | None:
    categories = sorted(set(human_scores) | set(ai_scores))
    if len(categories) < 2:
        return None
    category_index = {value: index for index, value in enumerate(categories)}
    human_counts = [0] * len(categories)
    ai_counts = [0] * len(categories)
    agreements = 0
    for human, ai in zip(human_scores, ai_scores):
        human_index = category_index[human]
        ai_index = category_index[ai]
        human_counts[human_index] += 1
        ai_counts[ai_index] += 1
        agreements += human_index == ai_index
    sample_count = len(human_scores)
    observed = agreements / sample_count
    expected = sum(
        human_count * ai_count
        for human_count, ai_count in zip(human_counts, ai_counts)
    ) / (sample_count * sample_count)
    if expected == 1:
        return None
    return (observed - expected) / (1 - expected)


def main() -> None:
    if not INPUT.exists() or INPUT.stat().st_size == 0:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        STATUS_OUTPUT.write_text(json.dumps({
            "status": "not_calculated",
            "paired_criterion_scores": 0,
            "reason": "No human/AI score pairs are available in data/human_marks.csv.",
            "metrics": None,
        }, indent=2), encoding="utf-8")
        print("No human score pairs available. No agreement metrics were calculated.")
        return
    with INPUT.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED - set(reader.fieldnames or [])
        rows = list(reader)
    if missing:
        raise SystemExit("human_marks.csv is missing columns: " + ", ".join(sorted(missing)))
    pairs = []
    for row in rows:
        try:
            human = float(row["human_score"])
            ai = float(row["ai_score"])
        except (ValueError, TypeError):
            continue
        pairs.append((row["assignment"], human, ai))
    if not pairs:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        STATUS_OUTPUT.write_text(json.dumps({
            "status": "not_calculated",
            "paired_criterion_scores": 0,
            "reason": "No human/AI score pairs are available in data/human_marks.csv.",
            "metrics": None,
        }, indent=2), encoding="utf-8")
        print("No complete human/AI score pairs available. No agreement metrics were calculated.")
        return
    human_scores = [row[1] for row in pairs]
    ai_scores = [row[2] for row in pairs]
    errors = [ai - human for human, ai in zip(human_scores, ai_scores)]

    def sample_variance(values: list[float]) -> float | None:
        if len(values) < 2:
            return None
        average = sum(values) / len(values)
        return sum((value - average) ** 2 for value in values) / (len(values) - 1)

    def pearson(left: list[float], right: list[float]) -> float | None:
        if len(left) < 2:
            return None
        left_mean, right_mean = sum(left) / len(left), sum(right) / len(right)
        left_ss = sum((value - left_mean) ** 2 for value in left)
        right_ss = sum((value - right_mean) ** 2 for value in right)
        if left_ss == 0 or right_ss == 0:
            return None
        return sum((a - left_mean) * (b - right_mean) for a, b in zip(left, right)) / math.sqrt(left_ss * right_ss)

    def quadratic_weighted_kappa(left: list[float], right: list[float]) -> float | None:
        categories = sorted(set(left) | set(right))
        if len(categories) < 2:
            return None
        index = {value: position for position, value in enumerate(categories)}
        size = len(categories)
        observed = [[0.0] * size for _ in range(size)]
        left_counts, right_counts = [0] * size, [0] * size
        for human, ai in zip(left, right):
            i, j = index[human], index[ai]
            observed[i][j] += 1
            left_counts[i] += 1
            right_counts[j] += 1
        n = len(left)
        observed_loss = expected_loss = 0.0
        for i in range(size):
            for j in range(size):
                weight = ((i - j) / (size - 1)) ** 2
                observed_loss += weight * observed[i][j] / n
                expected_loss += weight * left_counts[i] * right_counts[j] / (n * n)
        return None if expected_loss == 0 else 1 - observed_loss / expected_loss

    result = {
        "status": "calculated",
        "paired_criterion_scores": len(pairs),
        "assignments": len(set(row[0] for row in pairs)),
        "mae": sum(abs(error) for error in errors) / len(errors),
        "exact_agreement_rate": sum(error == 0 for error in errors) / len(errors),
        "deficiency_rate": sum(error != 0 for error in errors) / len(errors),
        "mean_signed_error_ai_minus_human": sum(errors) / len(errors),
        "variance_difference_ai_minus_human": (sample_variance(ai_scores) - sample_variance(human_scores)) if len(pairs) > 1 else None,
        "pearson_correlation": pearson(ai_scores, human_scores),
        "cohens_kappa": cohens_kappa(human_scores, ai_scores),
        "quadratic_weighted_kappa": quadratic_weighted_kappa(human_scores, ai_scores),
        "source": "data/human_marks.csv",
        "interpretation": "Computed from complete paired rows only; this is not a count of assignments processed.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    STATUS_OUTPUT.write_text(json.dumps({"status": "calculated", "paired_criterion_scores": len(pairs)}, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
