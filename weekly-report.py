from datetime import date
from dateutil.relativedelta import relativedelta, MO, SU
import requests
import json
import smtplib
import mimetypes
from email.message import EmailMessage
import os

today = date.today()
sunday = today + relativedelta(weekday=SU(-1))
last_monday = today + relativedelta(weekday=MO(-2))

url = "https://reports.api.clockify.me/v1/workspaces/6129e291f4c3bf0462173904/reports/detailed"

payload = json.dumps({
  "clients": {
    "contains": "CONTAINS",
    "ids": [
      ""
    ],
    "status": "ALL"
  },
  "dateRangeEnd": f"{str(sunday)}T23:59:59.000",
  "dateRangeStart": f"{str(last_monday)}T00:00:00.000",
  "detailedFilter": {
    "page": 1,
    "pageSize": 50
  },
  "exportType": "XLSX",
  "projects": {
    "contains": "CONTAINS",
    "ids": [
      "62168dc0b59ba47debba7505"
    ],
    "status": "ALL"
  },
  "amountShown": "HIDE_AMOUNT"
})
headers = {
  'X-Api-Key': os.getenv('X_API_KEY'),
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

with open('report.xlsx', 'wb') as output:
  output.write(response.content)

message = EmailMessage()
sender = os.getenv('SENDER')
recipient = os.getenv('RECIPIENT')
message['From'] = sender
message['To'] = recipient
message['Subject'] = 'Weekly Report'
body = """Dear Elham,
Please find the report file in the attachment.

Best Regards,
Omid
"""
message.set_content(body)
mime_type, _ = mimetypes.guess_type('report.xlsx')
mime_type, mime_subtype = mime_type.split('/')
with open('report.xlsx', 'rb') as file:
 message.add_attachment(file.read(),
 maintype=mime_type,
 subtype=mime_subtype,
 filename='report.xlsx')
mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
mail_server.set_debuglevel(1)
mail_server.login(sender, os.getenv('GOOGLE_APP_PWD'))
mail_server.send_message(message)
mail_server.quit()
