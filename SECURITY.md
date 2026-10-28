# Security

## The big rule

**Never commit, upload, or publish real case documents.** This public
repo contains only generated fake data. Real legal documents are
privileged and confidential; putting them in a public repository (or
sending them to a consumer AI service) can waive privilege and leak
personal data. If you adapt this for real work, run it locally, on
access-controlled storage, with a model/deployment your firm has
approved for confidential material.

## What the sorter itself does about safety

- Input is treated as hostile. Case numbers must match
  `^[A-Z]{1,3}-\d{4}-\d{1,5}$`, document types must be on a fixed
  allowlist, dates must parse as real dates and are re-formatted
  from the parsed value — a field can never smuggle `../`, a slash,
  or a shell fragment into a path or command (no shell is used).
- Output paths are resolved and verified to stay inside the chosen
  output directory before anything is written.
- Files are copied, never moved or deleted, and never overwritten;
  collisions get a numeric suffix.
- Anything that fails validation goes to `_NEEDS_REVIEW/` for a
  human. The tool never guesses.
- Files over 50 MB are refused rather than read unboundedly.
- `--dry-run` shows the plan without writing.
- Every run writes `_sort_log.csv`: original name, destination,
  extracted fields, status — the audit trail is part of the output,
  not an afterthought.

## Reporting a problem

Found a way to make the sorter write outside the output directory,
overwrite a file, or misroute a validated document? Open an issue
with a minimal fake example (never a real document).
