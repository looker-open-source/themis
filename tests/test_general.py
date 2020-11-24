import unittest
import re
import os
from urllib.request import urlopen
import ssl
from themis.modules.general import regex_base_url, get_looker_instance, format_output

class GeneralTestCase(unittest.TestCase):

    base_url = os.environ.get('LOOKERSDK_BASE_URL')

    def test_legacy_instance_url(self):
        self.assertEqual(regex_base_url('https://company.looker.com:19999'), 'https://company.looker.com', msg="Issue formatting url")

    def test_legacy_region_url(self):
        self.assertEqual(regex_base_url('https://company.eu.looker.com:19999'), 'https://company.eu.looker.com', msg="Issue formatting url")

    def test_legacy_api_url(self):
        self.assertEqual(regex_base_url('https://company.api.looker.com'), 'https://company.api.looker.com', msg="Issue formatting url")

    def test_legacy_op_url(self):
        self.assertEqual(regex_base_url('https://looker.company.com:19999'), 'https://looker.company.com', msg="Issue formatting url")

    def test_legacy_other_port_url(self):
        self.assertEqual(regex_base_url('https://looker.company.com:443'), 'https://looker.company.com', msg="Issue formatting url")

    def test_k8s_instance_url(self):
        self.assertEqual(regex_base_url('https://company.cloud.looker.com'), 'https://company.cloud.looker.com', msg="Issue formatting url")

    def test_k8s_region_url(self):
        self.assertEqual(regex_base_url('https://company.cloud.looker.com'), 'https://company.cloud.looker.com', msg="Issue formatting url")


    def test_looker_version(self):
        '''Pulls instance version to confirm >= 7.10''' 
        url = regex_base_url(str(self.__class__.base_url))
        request_data = urlopen(url + "/version",context=ssl._create_unverified_context()).read()
        instance_version = re.search(r'\d{1,2}\.{1}\d{1,2}', str(request_data))
        self.assertTrue(float(instance_version[0]) >= 7.10, msg="Issue with instance version")


    def test_format_output(self):
        '''Validates formatting of results is 20 items and a trailing `...`'''
        input_array = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w']
        self.assertTrue(len(format_output(input_array)) <= 21, msg="Issue formatting number of results of Looker functions")
        self.assertTrue(format_output(input_array)[-1] == "...", msg="Issue formatting trailing result of Looker functions")

    def test_format_no_output(self):
        '''Validates formatting of empty results'''
        input_array = []
        self.assertTrue(len(format_output(input_array)) == 1, msg="Issue formatting empty results of Looker functions") 
        self.assertTrue(format_output(input_array)[0] == 'No issues found.', msg="Issue formatting empty results of Looker functions")