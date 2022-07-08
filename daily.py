import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def google_client():
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'daily-accomplishments.json', scope
    )
    return gspread.authorize(creds)


def create_sheet():
    sheet = client.create("accomplishments")
    sheet.share('james.drabinsky@gmail.com', perm_type='user', role='writer')


def update_sheet():
    pass


scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'daily-accomplishments.json', scope
)
client = gspread.authorize(creds)


sheet = client.open("Daily Accomplishments").sheet1
sheet.get_all_records()