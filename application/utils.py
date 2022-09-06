
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template


SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "support@fca.com"
SENDER_PASSWORD = ""


def send_email(to, subject, message, content="Text", attachment=None):
    m = MIMEMultipart()
    m['To'] = to
    m['From'] = SENDER_ADDRESS
    m['Subject'] = subject
    m.preamble = "Reader does not support the format"

    if content == "html":
        m.attach(MIMEText(message, "html"))
    else:
        m.attach(MIMEText(message, "plain"))

    if attachment:
        with open(attachment, "rb") as attachment:
            # Add file as application/octet-stream
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        # Email attachments are sent as base64 encoded
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f"attachment; filename= {attachment}",
        )
        # Add the attchment to msg
        m.attach(part)

    mail_server = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    mail_server.login(SENDER_ADDRESS, SENDER_PASSWORD)

    mail_server.send_message(m)
    mail_server.quit()
    return True

def format_email_message(template_file, data={}, **kwargs):
    with open(template_file) as file_:
        template = Template(file_.read())
        return template.render(data=data, **kwargs)

# message = format_email_message("/Users/sp83/MyProjects/ProjectsOnTheWay/app_dev_2/project/FlashApplicationV2/templates/daily_notification.html", data={"name": "Raj", "email": "raj@example.com"})
# send_email(to='abc@gma.com', subject='FCA Review Reminder', message=message, content="html", attachment="/Users/sp83/MyProjects/ProjectsOnTheWay/app_dev_2/project/FlashApplicationV2/docs/Flash Card Application Helper.pdf")
