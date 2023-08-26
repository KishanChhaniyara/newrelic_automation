import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
import json
import csv
from email.message import EmailMessage
import ssl 
import smtplib

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('/app/client_secret.json', scope)
client = gspread.authorize(credentials)
file_name = f"New Relic alerts_{date.today()}"
folderId = '1DgeVbYr5Zuwy4_PpViJ0tvnlXOc2ruK_' # for specific folder
spreadsheet = client.create(file_name,folder_id=folderId)
worksheet = spreadsheet.add_worksheet(title="Monitor", rows=100, cols=20)

# importing the csv file in the monitor tab
spreadsheetId = spreadsheet.id  # Please set spreadsheet ID.
sheetName = 'Monitor'  # Please set sheet name you want to put the CSV data.
csvFile = '/app/kishannrql.csv'  # Please set the filename and path of csv file.

sh = client.open_by_key(spreadsheetId)
sh.values_update(
    sheetName,
    params={'valueInputOption': 'USER_ENTERED'},
    body={'values': list(csv.reader(open(csvFile)))}
)

#removing the Sheet file
worksheet = sh.sheet1
spreadsheet.del_worksheet(worksheet)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/%s" % spreadsheet.id

# Sending email using gmail
msg = """ Hi Team, Please find the below url

"""


email_sender = 'kishan.chhaniyara@embibe.com'
email_password = 'hhhkomjupbouvahm'
email_reciever = ['kishan.chhaniyara@embibe.com','']
subject = file_name 
body =  msg + spreadsheet_url

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_reciever
em['subject']= subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465 , context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender,email_reciever,em.as_string())