"""Step 2 – Mapping: decide which statement belongs to which customer.

    Type  : Manual: review the data carefully and finalise the mapping. Script: lists the PDFs and
            makes a first guess of the customer from the folder structure
    Input : <batch>/step1_intake/files/ (statement PDFs, in any folder structure)
    Output: <batch>/step2_mapping/mapping.xlsx – one row per PDF: customer, file, password;
            bank name stays empty (the system detects the bank)
    Next  : step3_upload

First guess of the customer:
  * PDF directly in the folder   → customer = file name
  * PDF inside <folder>/…        → customer = folder name        (group_level 1, default)
  * deeper nesting               → first two folders joined      (group_level 2)
  * group_level 0                → every PDF is its own customer
The guess is then reviewed and corrected by hand – e.g. statements from different bank folders
that belong to the same person are given the same customer.

Passwords: a password-protected PDF can only be processed if its password is provided; a PDF without
protection needs no password, so its password column stays blank.
Passwords from the file name (optional, --password-from-name): in the data received, some of the
password-protected PDFs came with the password inside the file name, separated by "_" (third part).
For those files the password is extracted from the name; files without it need no password:
    xyz_sbi_1234.pdf            → password 1234
    xyz_sbi_1234/statement.pdf  → password 1234 (taken from the folder name)

    python step2_mapping.py <batch_folder> [--group-level N] [--password-from-name]
"""
import argparse
from pathlib import Path

import pandas as pd

MAPPING_COLUMNS = ["customer_id", "file_path", "file_name", "password", "bank_name"]


def customer_for(rel_path, group_level):
    folders = rel_path.parts[:-1]
    if group_level == 0 or not folders:
        return "_".join([*folders, rel_path.stem]).replace(" ", "_")
    return "_".join(folders[:group_level])


def password_from_name(name):
    """Third "_"-separated part of a file or folder name, e.g. xyz_sbi_1234 → 1234."""
    parts = name.split("_")
    return parts[2] if len(parts) > 2 else ""


def password_for(rel_path):
    """Look at the top folder name first, then the file name."""
    folder = rel_path.parts[0] if len(rel_path.parts) > 1 else ""
    return password_from_name(folder) or password_from_name(rel_path.stem)


def is_password_protected(path):
    """An encrypted (password-protected) PDF carries an /Encrypt entry in the file."""
    return b"/Encrypt" in path.read_bytes()


def build_mapping(batch_dir, group_level=1, password_from_names=False):
    batch_dir = Path(batch_dir)
    files_dir = batch_dir / "step1_intake" / "files"
    out = batch_dir / "step2_mapping" / "mapping.xlsx"
    if out.exists():
        raise SystemExit(f"{out} already exists (it may have your edits)")

    pdfs = sorted(p for p in files_dir.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf")
    if not pdfs:
        raise SystemExit(f"No PDF files in {files_dir}")

    rows, missing = [], []
    for p in pdfs:
        rel = p.relative_to(files_dir)
        password = ""  # blank unless the PDF is password-protected
        if is_password_protected(p):
            password = password_for(rel) if password_from_names else ""
            if not password:
                missing.append(str(rel))
        rows.append({"customer_id": customer_for(rel, group_level), "file_path": str(rel),
                     "file_name": p.name, "password": password, "bank_name": ""})
    mapping = pd.DataFrame(rows, columns=MAPPING_COLUMNS)
    mapping.to_excel(out, index=False)
    print(f"{len(mapping)} PDFs, {mapping['customer_id'].nunique()} customers (first guess), "
          f"{(mapping['password'] != '').sum()} passwords filled in")
    if missing:
        print(f"{len(missing)} password-protected PDF(s) still need a password: {', '.join(missing)}")
    print(f"Review and correct {out} before uploading.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 2 – build the first-guess mapping")
    parser.add_argument("batch_folder")
    parser.add_argument("--group-level", type=int, default=1)
    parser.add_argument("--password-from-name", action="store_true")
    a = parser.parse_args()
    build_mapping(a.batch_folder, a.group_level, a.password_from_name)
