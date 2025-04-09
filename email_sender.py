import smtplib
from email.message import EmailMessage

def send_bulk_emails(sender_email, sender_password, recipients, subject, body):
    for name, company, email in recipients:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = email
        personalized_body = f"Hi {name},\n\n{body}\n\nRegards,\nYour Name"
        msg.set_content(personalized_body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
