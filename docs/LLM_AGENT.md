# LLM agent method — Muse / Hark-style, the judgment layer

The terminal, Excel, and Shortcuts versions all share one limit: they only
work when the metadata is clean and in the expected place. Real legal piles
aren't. Files are mislabeled, scanned crooked, named `FINAL_v2_ACTUALLY.pdf`,
or are a Motion with an Order stapled inside it.

That's the part a large language model agent (Muse, Hark, etc.) adds —
not speed on the clean files, **judgment on the dirty ones**.

## The workflow an agent runs

1. Inventory the folder (same as terminal — it literally uses the terminal).
2. For each file: extract text (OCR if scanned), then classify.
3. Sort + rename + log the confident ones automatically.
4. **Stop and flag the rest** instead of guessing.

## The prompt that does the classification

```
You are sorting legal documents into CaseNo/DocType/.
For the document text below, return ONLY JSON:
{"case_no": "", "case_name": "", "doc_type": "", "date_iso": "",
 "confidence": 0.0, "reason": "one line", "flags": []}

Rules:
- doc_type must be one of: Motion, Complaint, Exhibit, Deposition,
  Order, Correspondence, Invoice, Discovery, Other
- If the filename and the document content disagree, trust the CONTENT
  and add flag "name_content_mismatch".
- If two cases are mentioned, use the one in the caption and add
  flag "multiple_cases_mentioned".
- If you cannot determine case_no or doc_type, leave it blank,
  set confidence below 0.7, and say why in reason.
- Flag anything that looks privileged, sealed, or like it contains
  personal identifiers with flag "sensitive_review_first".
Do not invent a case number or a date.
```

## The routing rule (this is the whole safety design)

| Confidence / flags | Action |
|---|---|
| ≥ 0.85, no flags | Auto-sort, rename, log |
| 0.70–0.84, or name/content mismatch | Sort, but log for human spot-check |
| < 0.70, or `sensitive_review_first` | **Do not move it.** Put it in `_NEEDS_REVIEW` with the reason |

## What the agent does that the other three methods don't

- Reads a badly scanned deposition and still gets case + date right.
- Notices "this file named Invoice is actually a signed Order."
- Writes the audit log in plain English a paralegal can check.
- Can run the whole chain end to end: watch an inbox/folder → classify →
  sort → log → send a summary ("38 sorted, 2 need your eyes, here's why").

## The security caveat that is NOT optional for real case files

Client documents are privileged and confidential. Sending them to a random
consumer LLM account can waive privilege, leak personal data, and create a
discovery problem. A real deployment needs: an enterprise/local model with
no training on inputs, access controls per case, a full audit log, and a
human approving the exception queue. The demo uses 100% fake documents for
exactly this reason.
