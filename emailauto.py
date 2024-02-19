import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create message object
msg = MIMEMultipart()
msg['From'] = 'barnabas@drinking.co.uk'
msg['To'] = 'barnabaswhiting@gmail.com'
msg['Subject'] = 'Hello from Python'

# Message body
body = 'This is a test email sent from Python using smtplib.'
msg.attach(MIMEText(body, 'plain'))

# SMTP server details
smtp_server = 'mail.drinking.co.uk'
smtp_port = 465  # For SSL use 465, for TLS/STARTTLS use 587
username = 'barnabas@drinking.co.uk'
password = '_y8}Y1Fmsior'

# Send email
# Send email using SSL
try:
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.ehlo()
    server.login(username, password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    print('Email sent successfully')
except Exception as e:
    print(f'Failed to send email: {e}')