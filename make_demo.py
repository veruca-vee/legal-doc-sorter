#!/usr/bin/env python3
"""Generate a fake legal-document pile to practice sorting on.

100% invented cases, people, and documents. Standard library only,
works on Linux, macOS, Windows, and Android/Termux.

    python3 make_demo.py --count 400 --out legal-sort-demo
"""
import argparse
import csv
import random
from pathlib import Path

CASES = [
    ("Smith v. Jones", "CV-2024-118", "SmithJones"),
    ("Garcia v. Desert Rentals LLC", "CV-2025-042", "GarciaDesert"),
    ("State v. Miller", "CR-2024-089", "StateMiller"),
    ("Estate of Thompson", "PB-2025-017", "ThompsonEstate"),
]
DOC_TYPES = ["Motion", "Complaint", "Exhibit", "Deposition",
             "Order", "Correspondence", "Invoice", "Discovery"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=40)
    ap.add_argument("--out", type=Path, default=Path("legal-sort-demo"))
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    if not 1 <= args.count <= 100_000:
        raise SystemExit("--count must be between 1 and 100000")

    rng = random.Random(args.seed)
    unsorted = args.out / "unsorted"
    unsorted.mkdir(parents=True, exist_ok=True)
    rows = []
    for i in range(args.count):
        case_name, case_no, short = rng.choice(CASES)
        dtype = rng.choice(DOC_TYPES)
        year, month, day = rng.choice([2024, 2025]), rng.randint(1, 12), rng.randint(1, 28)
        date = f"{year}-{month:02d}-{day:02d}"
        name = rng.choice([
            f"{short} {dtype} FINAL v{rng.randint(1, 3)} ({i}).pdf",
            f"{month}-{day}-{year} {dtype} - {short} copy.pdf",
            f"SCAN_{1000 + i} {short} {dtype}.pdf",
            f"{dtype} {short} - DRAFT - {year}.{month:02d}.{day:02d}.pdf",
            f"{short}_{dtype}_{year}{month:02d}{day:02d}_signed.pdf",
        ])
        path = unsorted / name
        if path.exists():
            path = unsorted / f"{i}_{name}"
        path.write_text(
            f"FAKE DEMO DOCUMENT - NOT REAL\nCase: {case_name}\nCase No.: {case_no}\n"
            f"Document Type: {dtype}\nDate: {date}\n\n"
            "Simulated content for sorting practice only.\n", encoding="utf-8")
        rows.append([path.name, case_name, case_no, dtype, date])

    with open(args.out / "manifest_truth.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["original_filename", "case_name", "case_no", "doc_type", "date_iso"])
        w.writerows(rows)
    print(f"Created {len(rows)} fake documents in {unsorted}")
    print(f"Ground truth: {args.out / 'manifest_truth.csv'}")


if __name__ == "__main__":
    main()
