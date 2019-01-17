import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import datetime
import os

def email_tx(targetAddress, amount=0.00):
    serviceAddress = os.environ['email_addr']
    servicePassword = os.environ['email_pass']

    today = datetime.date.today().strftime('%d %b %Y')

    msg = MIMEMultipart()
    msg['From'] = serviceAddress
    msg['To'] = targetAddress
    msg['Subject'] = "CIMB Transaction Alerts"

    body = "Dear Sir / Madam\n\nWe refer to your request dated " + today + ". We would like to inform you that your transaction is successful.\n\nAmount: RM" + str(amount) + "\n\nShould you require any clarification, please do not hesitate to contact our Customer Service Hotline anytime at + 603 6204 7788.\n\nWe take this opportunity to thank you for using CIMB Clicks.\n\nCIMB Internet Banking\n\nPlease do not reply to this email as it is auto-generated."

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(serviceAddress, servicePassword)
    text = msg.as_string()
    server.sendmail(serviceAddress, targetAddress, text)

    print("Email sent.")
    server.quit()