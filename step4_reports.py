"""Step 4 – Reports: collect the Excel report for every account.

    Type  : Script + manual review
    Input : processed sessions from step 3
    Output: <batch>/step4_reports/round_1/ (for review), round_2/ (final, after corrections)
    Next  : step5_predictors

What happens:
  * one report per account found by the system – a customer with an SBI and a Baroda account gets
    two reports: <customer>__sbi__<account>.xlsx and <customer>__baroda__<account>.xlsx
  * round 1 is reviewed case by case; issues are highlighted and corrected
  * round 2 is the final set of reports

This step is carried out on the processing system; this file documents it.
"""
