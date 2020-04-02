import smtplib
import ssl
from email.message import EmailMessage


def sendMail(senderEmail, senderPassword, senderServer, smtpPort, recipient, messageContent):
    sender_email = senderEmail
    sender_password = senderPassword
    sender_server = senderServer

    message = EmailMessage()
    message["Subject"] = "Your Daily Samwat.ch Results"
    message["From"] = "Samwat.ch noreply@samwat.ch"
    message["To"] = recipient

    message.preamble = "Unfortunately, you need a MIME-aware mail reader to read Samwat.ch messages"
    message.set_content(messageContent, "html")

    context = ssl.create_default_context()
    print("Sending email to " + recipient)
    with smtplib.SMTP_SSL(sender_server, smtpPort, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(
            sender_email, recipient, message.as_string()
        )
