"""Step 3 – Upload: send each customer's statements for processing and follow up on failures.

    Type  : Script + manual check
    Input : <batch>/step2_mapping/mapping.xlsx (reviewed mapping: customer and file)
    Output: <batch>/step3_upload/ – upload summary (Success / Failed per file)
    Next  : step4_reports

What happens:
  * a session is created for each customer – this gives a session ID; the session holds all of that
    customer's statements (1 to many)
  * each statement is uploaded into the session with:
      - session ID   – required
      - the PDF      – required
      - password     – only if the PDF is password-protected
      - bank name    – optional, only if known; otherwise the system detects it
  * the system detects the bank, the account holder (identity) and the transactions
  * processing is started for each session
  * failures are checked in the upload summary: a statement counts as processed only if the
    system detected it and marked it complete
  * every failed file is investigated for its root cause, for example:
      - password missing or wrong        → correct password, upload again
      - invalid or damaged PDF           → ask for a valid copy
      - scanned (image) PDF              → ask for the original digital statement
      - not a bank statement             → exclude and report
      - format not supported yet         → raise it so support is added to the system, then re-process

This step is carried out on the processing system; this file documents it.
"""
