
from datetime import date
import base64
import os
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from sendgrid import SendGridAPIClient


def send_report_out(content):
    '''Processes the email content and sends it to recipients thru SendGrid'''
    try:
      # format env variable like: 'example1@mail.com,example2@mail.com'
        email_list = os.environ.get('THEMIS_EMAIL_RECIPIENTS')
        to_emails = []
        for email in email_list.split(','):
          to_emails.append(email)
    except Exception as e:
        print("Missing THEMIS_EMAIL_RECIPIENTS Variables {}".format(e))

    message = Mail(
        from_email = 'themisreport@example.com',
        to_emails = email_list,
        subject = 'LOOKER Instance Themis report for {}'.format(date.today().strftime("%d-%m-%Y")),
        html_content = content
        )

    file_path = './modules/rendering/final_attachment.pdf'
    with open(file_path, 'rb') as f:
        data = f.read()
        f.close()
    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('application/pdf')
    filename = "themis_details_{}".format(date.today().strftime("%Y%m%d"))
    attachment.file_name = FileName(filename)
    attachment.disposition = Disposition('attachment')
    attachment.content_id = ContentId('Example Content ID')
    message.attachment = attachment

    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        # https://sendgrid.com/docs/API_Reference/Web_API_v3/Mail/errors.html
        if response.status_code not in (200, 201, 202):
            print(response.status_code)
            print(response.body)
            print(response.headers)
    except Exception as e:
        print(e)
