# Excel / Google Sheets method

Sorting the *index* in a spreadsheet takes ~2 minutes for a whole batch,
even though Excel doesn't move the files itself.

1. Get the file list instantly: Power Query → From Folder (Excel), or
   `ls > list.csv` from a terminal.
2. Fill in `case_no`, `doc_type`, `date_iso` per row — Text to Columns
   and Flash Fill do most of it from messy filenames.
3. Live formulas build the rest for every row at once:
   - New filename: `=D2&"_"&C2&"_"&B2&".pdf"`
   - Destination:  `=B2&"/"&C2&"/"&E2`
   - Status:       `=IF(OR(B2="",C2="",D2=""),"NEEDS REVIEW","READY")`
4. Sort by destination, filter `NEEDS REVIEW` for the exceptions.

Limits: it can't read inside a scanned PDF (a human, OCR, or an LLM
supplies those columns for messy scans), and something else — the
terminal sorter, Shortcuts, or an agent — still has to move the files.
