import smtplib as smtp
from email.message import EmailMessage
from os import getenv


URL = "smtp.gmail.com"
PORT = 587

login = {
    "email": "rbcmlproject@gmail.com",
    "passwd": getenv("EMAIL_PASSWORD")
}

def send(subject, content, receiver_email):
    message = EmailMessage()
    message["From"] = login["email"]
    message["To"] = receiver_email 
    message["Subject"] = subject
    message.set_content(content)

    try:
        server = smtp.SMTP(URL, PORT)
        server.starttls()
        server.login(login["email"], login["passwd"])
        server.send_message(message)
        server.quit()

    except Exception as e:
        return e
