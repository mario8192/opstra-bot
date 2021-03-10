import sys
import gspread
import gspread_formatting as gsf
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)


def work(sheet_date, table):
    print(table)

    # sheet = client.open("Opstra Analytics").worksheet(sheet_date)

    return
