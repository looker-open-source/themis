import unittest
from modules.email_content import email_body


class SendEmailTestCase(unittest.TestCase):


    def test_email_body(self):
        results = email_body('test.looker.com', '7.18', '12', 6, 15, 20, 1, 7, 25, 30)
        data = '''
                Today's Report:<br><br>
                Looker instance: test.looker.com<br>
                Looker version: 7.18
                <br>
                <br>👤  <strong><font color="#4d5170" size="4">Users Summary</font></strong><br>
                    12 users in the instance.
                <hr>
                <br>💻  <strong><font color="#4d5170" size="4">Projects LookML Validation</font></strong><br>
                    6 projects in the instance.
                <hr>
                <br>📊  <strong><font color="#4d5170" size="4">Content Validation</font></strong><br>
                    15 content with errors in the instance.
                <hr>
                <br>📩️  <strong><font color="#4d5170" size="4">Schedules</font></strong><br>
                    20 schedules in the instance.
                <hr>
                <br>🚧  <strong><font color="#4d5170" size="4">PDTs</font></strong><br>
                    1PDTs build failures in the instance (<i>Greater than number of PDTs failing</i>).
                <hr>
                <br>🔑  <strong><font color="#4d5170" size="4">Connectivity</font></strong><br>
                    7 connections in the instance.<br>
                    25 integrations in the instance.<br>
                    30 datagroups in the instance.<br>
                <br><br>
                <font color="grey" size="1">
                    Find more information <a href="https://github.com/looker-open-source/Themis">go to the repo</a>
                <br>
                    Something Wrong? <a href="https://github.com/looker-open-source/Themis">Tell us</a>
                </font>'''
        self.assertEqual(results, data, msg="Issue formatting email body")
