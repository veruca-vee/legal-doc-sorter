# legal-doc-sorter

**Sorting case documents by hand is a pattern-matching loop — and
pattern-matching loops are what computers are for.**

In a lot of legal offices, a pile of documents lands in one folder with
names like `SmithJones motion FINAL v2 (26).pdf`, `SCAN_1017 SmithJones
Complaint.pdf`, `1-3-2024 Invoice - SmithJones copy.pdf` — and a person
opens each one, works out which case / what type / what date it is,
renames it, and drags it into a folder. One file at a time.

This repo is a small, safe, multi-OS demo of doing that job in seconds,
four different ways. All sample data is **100% fake** (invented cases,
invented people). See [SECURITY.md](SECURITY.md) before ever pointing
any tool like this at real case files.

## Quick start (any OS)

Needs only Python 3.8+ — standard library, no installs, no network.

**Linux / macOS / Android (Termux):**
```bash
python3 make_demo.py --count 400        # build a messy fake pile
python3 sort_docs.py legal-sort-demo/unsorted sorted_output
cat sorted_output/_sort_log.csv
```

**Windows (PowerShell or cmd):**
```powershell
py make_demo.py --count 400
py sort_docs.py legal-sort-demo\unsorted sorted_output
type sorted_output\_sort_log.csv
```
Wrappers `sort_docs.sh` / `sort_docs.bat` do the same thing.

Result format: `CaseNo/DocType/YYYY-MM-DD_DocType_CaseNo.pdf`,
copied (never moved, never overwritten), with an audit log, and
anything unparseable diverted to `_NEEDS_REVIEW/` instead of being
guessed at. `--dry-run` reports without writing anything.

## Measured results (400 fake files)

| Method | Time | Notes |
|---|---|---|
| By hand | hours *(estimate at 30–60 sec/file)* | Plus fatigue errors, no log |
| This Python sorter, Linux VM | **0.62 s** | All 400 sorted, log written |
| This Python sorter, budget Android phone (Termux) | **2.56 s** | Same code, verified on-device |
| Earlier bash sorter, same VM | 9.9 s | One grep/awk process per field per file |
| Earlier bash sorter, same Android phone | 84 s | Same reason — process startup is slow there |

The Python version is ~16× faster than the bash one on the VM and
~33× faster on the phone, because it reads each file once in-process
instead of spawning tools per file.

## The same job, four ways

| Method | Doc |
|---|---|
| Terminal / Python | this README + `sort_docs.py` |
| Excel / Google Sheets | [docs/EXCEL.md](docs/EXCEL.md) — live formulas build every new filename at once |
| Apple Shortcuts | [docs/APPLE_SHORTCUTS.md](docs/APPLE_SHORTCUTS.md) — no-code, on-device |
| LLM agent (Muse / Hark-style) | [docs/LLM_AGENT.md](docs/LLM_AGENT.md) — judgment for messy scans, with a confidence gate |

The first three only work when metadata is clean and where it's
expected. The LLM version adds judgment for the dirty files — and the
security caveats that come with that are in the doc, not footnoted away.

## Tests

```bash
python3 -m unittest discover -s tests -v
```
Covers: normal sorting, a path-traversal case number
(`../../evil` → review queue, nothing written outside the output),
bad dates, unknown document types, and never overwriting / never
deleting the originals.

## License

MIT — see [LICENSE](LICENSE). By Veruca Velharin.
