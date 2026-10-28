"""Run:  python3 -m unittest discover -s tests -v   (stdlib only)"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import sort_docs


def write_doc(folder, name, case_no="CV-2024-118", dtype="Motion", date="2025-04-08"):
    p = Path(folder) / name
    p.write_text(f"FAKE\nCase No.: {case_no}\nDocument Type: {dtype}\nDate: {date}\n",
                 encoding="utf-8")
    return p


class SortTests(unittest.TestCase):
    def test_sorts_valid_doc(self):
        with tempfile.TemporaryDirectory() as td:
            src, out = Path(td) / "in", Path(td) / "out"
            src.mkdir(); write_doc(src, "messy FINAL v2 (1).pdf")
            ok, review = sort_docs.sort_folder(src, out)
            self.assertEqual((ok, review), (1, 0))
            self.assertTrue((out / "CV-2024-118" / "Motion"
                             / "2025-04-08_Motion_CV-2024-118.pdf").exists())
            self.assertTrue((out / "_sort_log.csv").exists())

    def test_traversal_case_number_goes_to_review_not_outside(self):
        with tempfile.TemporaryDirectory() as td:
            src, out = Path(td) / "in", Path(td) / "out"
            src.mkdir(); write_doc(src, "evil.pdf", case_no="../../evil")
            ok, review = sort_docs.sort_folder(src, out)
            self.assertEqual((ok, review), (0, 1))
            self.assertTrue((out / "_NEEDS_REVIEW" / "evil.pdf").exists())
            self.assertFalse((Path(td) / "evil").exists())

    def test_bad_date_and_unknown_type_go_to_review(self):
        with tempfile.TemporaryDirectory() as td:
            src, out = Path(td) / "in", Path(td) / "out"
            src.mkdir()
            write_doc(src, "baddate.pdf", date="2025-13-40")
            write_doc(src, "badtype.pdf", dtype="Banana")
            ok, review = sort_docs.sort_folder(src, out)
            self.assertEqual((ok, review), (0, 2))

    def test_never_overwrites(self):
        with tempfile.TemporaryDirectory() as td:
            src, out = Path(td) / "in", Path(td) / "out"
            src.mkdir()
            write_doc(src, "a.pdf"); write_doc(src, "b.pdf")
            sort_docs.sort_folder(src, out)
            files = list((out / "CV-2024-118" / "Motion").glob("*.pdf"))
            self.assertEqual(len(files), 2)
            # originals still in place: copy, never move/delete
            self.assertEqual(len(list(src.glob("*.pdf"))), 2)


if __name__ == "__main__":
    unittest.main()
