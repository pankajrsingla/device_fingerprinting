#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
unit_tests.py: testcases to test the functionality of the FingerprintHandler class as well as the Flask app.
"""

# Import modules
import unittest
from fingerprint_handler import FingerprintHandler
from app import app

class FingerprintHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.fingerprint_handler = FingerprintHandler()

    def test_get_fingerprints(self):
        """Test the get_fingerprints() function."""
        fingerprints = self.fingerprint_handler.get_fingerprints()
        self.assertIsInstance(fingerprints, list)
        self.assertEqual(len(fingerprints), 246)     
        fingerprint_keys = set(tuple(fingerprint.keys()) for fingerprint in fingerprints)
        self.assertEqual(fingerprint_keys, {('pattern', 'description', 'examples', 'params')})

    def test_get_md5_hash(self):
        """Test the get_md5_hash() function."""
        content = "Device_Fingerprinting_Pankaj"
        md5_hash = self.fingerprint_handler.get_md5_hash(content.encode())
        self.assertIsInstance(md5_hash, str)
        self.assertEqual(md5_hash, "337b6de1f5e7f81def9e2ae36f323ada")

    def test_get_matching_fingerprints(self):
        """Test the get_matching_fingerprints() function."""
        queried_md5 = "55ece828b1329741c1d553a6575d71f1"
        matching_description = self.fingerprint_handler.get_matching_fingerprints(queried_md5)[0]["description"]
        self.assertIsInstance(matching_description, str)
        self.assertEqual(matching_description, "Radarr")        

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home(self):
        """Test the home page for the app."""
        response = self.app.get('/')
        response_text = str(response.data)
        self.assertEqual(response_text, "b'Hello, visitor!'")

    def test_fingerprint_get_method(self):
        """Test the device_fingerprinting() functionality using the GET method."""
        response = self.app.get('/check_fingerprint?targets=www.google.com')
        self.assertEqual(response.status_code, 200)
        response_text = str(response.data)
        self.assertIn('"Matches":[{"description":"Google - Homepage', response_text)        

    def test_fingerprint_post_method(self):
        """Test the device_fingerprinting() functionality using the POST method with both valid and invalid inputs."""
        valid_targets = ["www.google.com", "172.253.123.147", "185.199.112.2"]
        invalid_targets = ["ww.as.eededede", "1254.5445454.54.57", "https://github.com/drupal/drupal/blob/f0a16bf2a4d1524aa33b656533e37d977cca4802/core/misc/"]
        payload = {"targets": valid_targets + invalid_targets}
        response = self.app.post('http://127.0.0.1:5000/check_fingerprint', json=payload)
        response_text = str(response.data)
        self.assertIn('IP_Address":"185.199.112.2","Matches":[{"description":"Ubiquiti WAP (Vague)', response_text)        

if __name__ == '__main__':
    unittest.main()