"""Configure google sheet api"""

import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .crendential import load_credential

logger = logging.getLogger(__name__)

def get_from_sheet(sheet_id, sheet_range, cred_folder=None):
    """Get a range of values from google sheet"""
    cred = load_credential(cred_folder=cred_folder)
    try:
        service = build('sheets', 'v4', credentials=cred)
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=sheet_id,
            range=sheet_range
        ).execute()
        return result.get('values', [])
    except HttpError as err:
        logger.error(err)

def append_to_sheet(sheet_id, sheet_range, values, value_input_option='RAW', cred_folder=None):
    """Append a row to google sheet"""
    cred = load_credential(cred_folder=cred_folder)
    try:
        service = build('sheets', 'v4', credentials=cred)
        sheet = service.spreadsheets()
        result = sheet.values().append(
            spreadsheetId=sheet_id,
            range=sheet_range,
            valueInputOption=value_input_option,
            body={
                'values': values
            }
        ).execute()
    except HttpError as err:
        logger.error(err)