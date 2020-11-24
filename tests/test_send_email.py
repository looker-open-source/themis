import unittest
import os, json
import ssl
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment)

class SendgridTestCase(unittest.TestCase):

    sg_key = os.environ.get('SENDGRID_API_KEY')
    sendgrid_client = SendGridAPIClient(sg_key)

    def test_sendgrid_env_var_format(self):
        '''Tests if SendGrid API key starts with `SG.`'''
        self.assertEqual(self.__class__.sg_key[:3], "SG.", msg="SendGrid API Key Not Found or Wrong Format")
        

    def test_sending_one_recipient(self):
        '''Testing Sendgrid email to one recipient'''
        # Omits SSL verification https://www.python.org/dev/peps/pep-0476/
        ssl._create_default_https_context = ssl._create_unverified_context
        message = Mail(
            from_email = 'test@example.com',
            to_emails = 'john.doe@example.com',
            subject = 'Testing SendGrid',
            html_content = '<strong>Themis Testing</strong>'
            ) 
        response = self.__class__.sendgrid_client.send(message)
        self.assertEqual(response.status_code, 202, msg="Sending Email to 1 Recipient Failed")


    def test_single_email_to_many_recipients(self):
        '''Testing Sendgrid email to multiple recipients'''
        # Omits SSL verification https://www.python.org/dev/peps/pep-0476/
        ssl._create_default_https_context = ssl._create_unverified_context
        message = Mail(
            from_email = 'test@example.com',
            to_emails = 'john.doe@example.com,jane.doe@example.com,joe@example.com',
            subject = 'Testing SendGrid',
            html_content = '<strong>Themis Testing</strong>'
            ) 
        response = self.__class__.sendgrid_client.send(message)
        self.assertEqual(response.status_code, 202, msg="Sending Email to many Recipients Failed")