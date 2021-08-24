import gspread
from oauth2client.service_account import ServiceAccountCredentials

def authorize(secret):
    #START: Connecting to Google Sheets with Credentials
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(secret, scope)
    client = gspread.authorize(creds)
    return client
    #sheet = client.open("Recurring Payments").worksheet("Input")