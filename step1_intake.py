"""Step 1 – Intake: capture the requirements and set up a folder for the batch.

    Type  : Manual: talk to the client. Script: creates the batch folder + intake form
    Input : client conversation – what do they want to evaluate (fraud / identity / transactions /
            indicators), how many files are they sharing
    Output: <batch>/step1_intake/requirements.yaml (filled-in intake form)
            <batch>/step1_intake/files/          (the statement PDFs received)
            empty folders for steps 2 … 6
    Next  : step2_mapping

    python step1_intake.py <batch_folder>
"""
import sys
from datetime import date
from pathlib import Path

STEP_FOLDERS = ["step1_intake/files", "step2_mapping", "step3_upload",
                "step4_reports", "step5_predictors", "step6_delivery"]
INTAKE_FORM = Path(__file__).with_name("intake_template.yaml")


def create_batch(batch_dir):
    batch_dir = Path(batch_dir)
    if batch_dir.exists():
        raise SystemExit(f"{batch_dir} already exists")
    for folder in STEP_FOLDERS:
        (batch_dir / folder).mkdir(parents=True)
    form = INTAKE_FORM.read_text()
    form = form.replace("{{client_name}}", batch_dir.name).replace("{{today}}", date.today().isoformat())
    (batch_dir / "step1_intake" / "requirements.yaml").write_text(form)
    print(f"Created {batch_dir}: fill in step1_intake/requirements.yaml and put the PDFs in step1_intake/files/")


if __name__ == "__main__":
    create_batch(sys.argv[1])
