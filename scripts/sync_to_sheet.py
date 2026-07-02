#!/usr/bin/env python3
"""Append new ReachOut sponsor prospects from data/prospects.csv to the canonical Google Sheet.

Append-only by design: only rows for companies not already present in the sheet
are added. Existing rows are never overwritten, updated, or removed here, so the
sheet accumulates every prospect ever found across every run rather than being
replaced by each new set of sources.

Requires:
  GOOGLE_SHEET_ID            - the target spreadsheet's ID (from its URL)
  GOOGLE_SERVICE_ACCOUNT_JSON - full JSON key of a service account with Editor
                                access to that spreadsheet
"""
import csv
import json
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build

CSV_PATH = "data/prospects.csv"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def main():
    sheet_id = os.environ["GOOGLE_SHEET_ID"]
    creds = service_account.Credentials.from_service_account_info(
        json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]), scopes=SCOPES
    )
    service = build("sheets", "v4", credentials=creds)
    values = service.spreadsheets().values()

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        print("prospects.csv is empty, nothing to sync")
        return
    header, data_rows = rows[0], rows[1:]

    sheet_meta = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    sheet_title = sheet_meta["sheets"][0]["properties"]["title"]

    existing = values.get(spreadsheetId=sheet_id, range=f"{sheet_title}!A:A").execute().get("values", [])
    existing_companies = {row[0].strip().lower() for row in existing[1:] if row}

    if not existing:
        values.append(
            spreadsheetId=sheet_id,
            range=f"{sheet_title}!A1",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": [header]},
        ).execute()
        existing_companies = set()

    new_rows = [row for row in data_rows if row and row[0].strip().lower() not in existing_companies]

    if not new_rows:
        print("No new prospects to append to the Google Sheet.")
        return

    values.append(
        spreadsheetId=sheet_id,
        range=f"{sheet_title}!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": new_rows},
    ).execute()
    print(f"Appended {len(new_rows)} new prospect(s) to the Google Sheet: " + ", ".join(r[0] for r in new_rows))


if __name__ == "__main__":
    main()
