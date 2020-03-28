# Email imports
import smtplib
import ssl
from email.message import EmailMessage


def createSever(senderEmail, senderPassword, senderServer):
    sender_email = senderEmail
    sender_password = senderPassword
    sender_server = senderServer
