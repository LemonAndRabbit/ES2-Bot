"""Configure google sheet api"""

import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .crendential import load_credential

def get_from_sheet(sheet_id, sheet_range):
    """Get a range of values from google sheet"""
    cred = load_credential()
    try:
        service = build('sheets', 'v4', credentials=cred)
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=sheet_id,
            range=sheet_range
        ).execute()
        return result.get('values', [])
    except HttpError as err:
        logging.error(err)

def append_to_sheet(sheet_id, sheet_range, values):
    """Append a row to google sheet"""
    cred = load_credential()
    try:
        print(sheet_id)
        print(sheet_range)
        print(values)
        service = build('sheets', 'v4', credentials=cred)
        sheet = service.spreadsheets()
        result = sheet.values().append(
            spreadsheetId=sheet_id,
            range=sheet_range,
            valueInputOption='RAW',
            body={
                'values': values
            }
        ).execute()
    except HttpError as err:
        logging.error(err)
