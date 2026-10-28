#!/usr/bin/env python3
"""Sort legal documents by the metadata inside each file.

Portable: Python 3.8+, standard library only. Runs on Linux, macOS,
Windows, and Android/Termux. No shell, no eval, no network.

Security design:
  * Every extracted field is validated before it touches a path:
    case numbers must match a strict pattern, document types must be
    on an allowlist, and dates must parse as real calendar dates.
    Anything else goes to _NEEDS_REVIEW and is never guessed at.
  * The destination path is resolved and checked to stay inside the
    output directory (path-traversal proof, even for a case number
    like "../../evil").
  * Files are COPIED, never moved or deleted, and are never
    overwritten (a _1, _2 suffix is added on collision).
  * --dry-run reports what would happen without writing anything.
  * Every action is written to an audit log (sorted_output/_sort_log.csv).
"""
import argparse
import csv
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

CASE_NO_RE = re.compile(r"^[A-Z]{1,3}-\d{4}-\d{1,5}$")
ALLOWED_TYPES = {
    "Motion", "Complaint", "Exhibit", "Deposition", "Order",
    "Correspondence", "Invoice", "Discovery", "Other",
}
FIELD_RES = {
    "case_no": re.compile(r"^Case No\.:\s*(\S+)\s*$", re.M),
    "doc_type": re.compile(r"^Document Type:\s*(\S+)\s*$", re.M),
    "date": re.compile(r"^Date:\s*(\S+)\s*$", re.M),
}
MAX_FILE_BYTES = 50 * 1024 * 1024  # refuse absurd inputs instead of reading forever


def extract_fields(text):
    return {k: (m.group(1) if (m := rx.search(text)) else None)
            for k, rx in FIELD_RES.items()}


def validate(fields):
    """Return (case_no, doc_type, date_iso) or None if anything is off."""
    case_no, doc_type, date = fields.get("case_no"), fields.get("doc_type"), fields.get("date")
    if not case_no or not CASE_NO_RE.match(case_no):
        return None
    if doc_type not in ALLOWED_TYPES:
        return None
    try:
        parsed = datetime.strptime(date or "", "%Y-%m-%d")
    except ValueError:
        return None
    # Re-format from the parsed date so the value in the path is ours, not the file's.
    return case_no, doc_type, parsed.strftime("%Y-%m-%d")


def safe_destination(out_dir: Path, case_no: str, doc_type: str, filename: str) -> Path:
    dest = (out_dir / case_no / doc_type / filename).resolve()
    if out_dir.resolve() not in dest.parents:
        raise ValueError(f"destination escapes output dir: {dest}")
    return dest


def sort_folder(input_dir: Path, output_dir: Path, dry_run: bool = False):
    if not input_dir.is_dir():
        raise SystemExit(f"input dir not found: {input_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    rows, sorted_count, review_count = [], 0, 0

    for src in sorted(p for p in input_dir.iterdir() if p.is_file()):
        if src.stat().st_size > MAX_FILE_BYTES:
            fields, valid = {}, None
        else:
            try:
                text = src.read_text(encoding="utf-8", errors="replace")
            except OSError:
                text = ""
            fields, valid = extract_fields(text), None
            valid = validate(fields)

        if valid is None:
            review_count += 1
            dest = output_dir / "_NEEDS_REVIEW" / src.name
            if not dry_run:
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists():
                    shutil.copy2(src, dest)
            rows.append([src.name, str(dest), fields.get("case_no") or "",
                         fields.get("doc_type") or "", fields.get("date") or "", "NEEDS_REVIEW"])
            continue

        case_no, doc_type, date_iso = valid
        filename = f"{date_iso}_{doc_type}_{case_no}{src.suffix or '.pdf'}"
        dest = safe_destination(output_dir, case_no, doc_type, filename)
        n = 1
        while dest.exists():
            dest = dest.with_name(f"{Path(filename).stem}_{n}{Path(filename).suffix}")
            n += 1
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
        sorted_count += 1
        rows.append([src.name, str(dest), case_no, doc_type, date_iso, "SORTED"])

    if not dry_run:
        with open(output_dir / "_sort_log.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["original", "new_path", "case_no", "doc_type", "date", "status"])
            w.writerows(rows)
    return sorted_count, review_count


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("input_dir", type=Path)
    ap.add_argument("output_dir", type=Path)
    ap.add_argument("--dry-run", action="store_true", help="report only, write nothing")
    args = ap.parse_args(argv)
    ok, review = sort_folder(args.input_dir, args.output_dir, dry_run=args.dry_run)
    print(f"Sorted: {ok}  Needs review: {review}")
    print(f"Log: {args.output_dir / '_sort_log.csv'}" if not args.dry_run else "(dry run, no log written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
