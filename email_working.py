import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(recipient, text, user, password):
    server = 'mx.kdv37.ru'

    sender = user
    subject = 'Заявка на вступление в СРО от бота'

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['Bcc'] = sender

    part_html = MIMEText(text, 'plain',  'utf-8')
    msg.attach(part_html)

    mail = smtplib.SMTP_SSL(server)
    mail.login(user, password)
    mail.sendmail(sender, recipient, msg.as_string())
    mail.quit()

if __name__ == "__main__":
    send_mail(
        text="test",
        recipient="sizovad@ivgpu.com",
        user="info@iossro37.ru",
        password=r"G5bs36%u8w"
    )