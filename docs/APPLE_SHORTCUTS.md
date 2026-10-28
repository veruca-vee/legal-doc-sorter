# Apple Shortcuts method — no code, ~5 min to build, seconds to run

Same job, on an iPhone/iPad/Mac, using only Shortcuts + Files. This is the
"even a phone can do this" proof.

## Build it once

1. **Receive** — Shortcuts → New → Add "Select File" (turn on Select Multiple),
   or set it to receive Files from the Share Sheet.
2. **Repeat with Each** — everything below happens inside this loop.
3. **Get Text from Input** — for a scan/photo, use "Extract Text from Image"
   first, then this. (Built-in OCR, no app needed.)
4. **Match Text** — three matches on that text, with these patterns:
   - Case No.: `Case No\.: ([A-Z]+-\d+-\d+)`
   - Type: `Document Type: (\w+)`
   - Date: `Date: (\d{4}-\d{2}-\d{2})`
   Get the first match's Group 1 from each.
5. **If** — if any of the three matches is empty, move the file to a
   `_NEEDS_REVIEW` folder and skip to the next repeat item. Do not guess.
6. **Create Folder** — Files / Sorted / [Case No.] / [Doc Type]
   (Shortcuts creates it if it doesn't exist.)
7. **Rename File** — to `[Date]_[Type]_[Case No.]`
8. **Move File** — to the folder from step 6.
9. **End Repeat** → **Show Notification**: "Sorted N files."

## What it proves, and where it breaks

- Proves: the sorting logic is so simple a no-code phone automation does it.
  Nobody needed to drag 40 files one by one.
- Breaks on: messy OCR, a caption page that names two cases, weird date
  formats the regex doesn't expect. It has no judgment — it matches patterns
  or it fails.
- Security note (the part usually skipped): this version runs **on-device**,
  which is actually its one real advantage. The tradeoff is there's no audit
  log, no permissions model, and no record of who moved what — a problem for
  real case files, fine for a demo.
