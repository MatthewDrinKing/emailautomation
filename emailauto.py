import sqlite3
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
email_config = config['email']

# Function to send email
def send_email(recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = email_config['smtp_user']
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
        server.starttls()
        server.login(email_config['smtp_user'], email_config['smtp_password'])
        server.sendmail(email_config['smtp_user'], recipient_email, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")

# Main function to query the database and send emails
def main():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT email FROM contacts WHERE emailsent = 0")
    contacts = cursor.fetchall()
    
    for contact in contacts:
        email = contact[0]
        send_email(email, "Your Subject Here", "Your email body here.")
        
        # Update the 'emailsent' status
        cursor.execute("UPDATE contacts SET emailsent = 1 WHERE email = ?", (email,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
