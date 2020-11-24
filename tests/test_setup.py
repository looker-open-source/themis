import unittest
import os, re
from pathlib import Path

class LookerSDKTestCase(unittest.TestCase):

    base_url = os.environ.get('LOOKERSDK_BASE_URL')
    api_id = os.environ.get('LOOKERSDK_CLIENT_ID')
    api_secret = os.environ.get('LOOKERSDK_CLIENT_SECRET')
    email_list = os.environ.get('EMAIL_RECIPIENTS')
    sg_key = os.environ.get('SENDGRID_API_KEY')

    def test_looker_credentials(self):
        '''Tests if a looker.ini file is created in the top level dir. Will fail if using env var'''
        parent_dir = Path(__file__).parents[1]
        cred_file = []
        for file in os.listdir(parent_dir):
            if file.endswith(".ini"):
                cred_file.append(os.path.join(parent_dir, file))
        self.assertTrue(cred_file or self.__class__.base_url and self.__class__.api_id and self.__class__.api_secret, msg="Looker Credentials Not Found")
    

    def test_recipients_env_var(self):
        '''Tests if recipient email list environmnent variables exists'''
        self.assertIsNotNone(self.__class__.email_list, msg="Email Recipient Var Not Found")


    def test_emails_format(self):
        '''Tests the format for recipient emails'''
        email_format_ok = []
        for email in self.__class__.email_list.split(','):
            regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
            email = email.strip()
            if not (re.search(regex, str(email))):
                email_format_ok.append(email_format_ok)
        self.assertTrue(len(email_format_ok) == 0)


    def test_sendgrid_env_var(self):
        '''Tests if SendGrid API key exists'''
        self.assertIsNotNone(self.__class__.sg_key, msg="SendGrid API Key Not Found or Wrong Format")
    