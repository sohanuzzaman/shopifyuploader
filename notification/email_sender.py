import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv('../.env')

password = os.getenv('EMAIL_PASSWORD')

def send_email(to_email="subrankovicova@gmail.com"):
    # Zoho email credentials
    from_email = "mohan@sohanuzzaman.com"

    # Zoho SMTP server settings
    smtp_server = "smtp.zoho.com"  # Gunakan "smtppro.zoho.com" untuk alamat email berbasis domain
    port = 587  # Gunakan 465 untuk SSL

    # Set up the SMTP server
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()  # Call this for TLS
    server.login(from_email, password)

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "New products uploaded to shopify please login and process them"
    msg.attach(MIMEText("Hi Stana, there are new products added to shopify through our automated python script. Please login to https://admin.shopify.com/ then sync the new product to etsy and update the title, description and other info", 'plain'))

    # Send the email
    server.send_message(msg)
    server.quit()

# Contoh penggunaan
send_email()
