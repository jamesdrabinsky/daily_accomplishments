import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('daily-accomplishments.json', scope)
# with open('daily-accomplishments.json') as f:
#     creds = json.load(f)
client = gspread.authorize(creds)
print(client)