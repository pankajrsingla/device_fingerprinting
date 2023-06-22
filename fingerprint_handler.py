#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fingerprint_handler.py: defines the FingerprintHandler class for handling fingerprinting of favicons based on their IP addresses.
"""

# Import modules
import re
import hashlib
import requests
from bs4 import BeautifulSoup
import ipaddress
import socket

class FingerprintHandler:
    def __init__(self):
        """Initialize the FingerprintHandler object by loading the fingerprints."""
        self.fingerprints = self.get_fingerprints()

    def get_fingerprints(self):
        """
        Load and return fingerprints from the favicons.xml file.
        Returns:
            rapid7_fingerprints (list): A list of dictionaries representing the fingerprints.
        """
        rapid7_fingerprints = []
        xml_file = 'favicons.xml'
        with open(xml_file, 'r') as file:
            soup = BeautifulSoup(file, 'xml')
            # Find all the "fingerprint" tags in the XML file
            all_entries = soup.find_all('fingerprint')
            for entry in all_entries:
                fingerprint = {}
                fingerprint['pattern'] = entry['pattern']
                fingerprint['description'] = entry.find('description').text
                # Extract the "example" elements from the "fingerprint" tag and store them as a list
                fingerprint['examples'] = [example.text for example in entry.find_all('example')]
                fingerprint['params'] = []
                # Iterate through the param tags and extract the "pos", "name", and "value" attributes
                for param_tag in entry.find_all('param'):
                    param_info = {
                        'pos': int(param_tag['pos']),
                        'name': param_tag['name'],
                        'value': param_tag['value']
                    }
                    fingerprint['params'].append(param_info)
                rapid7_fingerprints.append(fingerprint)    
        return rapid7_fingerprints
    
    def get_md5_hash(self, file_content):
        """
        Calculate the MD5 hash of the given file content.
        Args:
            file_content (bytes): The content of the file.
        Returns:
            str: The MD5 hash of the file content as a hexadecimal string.
        """
        # Create an instance of the MD5 hash object
        md5_hash = hashlib.md5()
        # Update the hash object with the file content
        md5_hash.update(file_content)
        # Return the hexadecimal representation of the MD5 hash
        return md5_hash.hexdigest()
    
    def get_matching_fingerprints(self, queried_md5):
        """
        Match the queried MD5 hash against the stored fingerprints and return the matching ones.
        Args:
            queried_md5 (str): The MD5 hash to be matched.
        Returns:
            list: A list of dictionaries representing the matching fingerprints.
                Each dictionary contains 'description', 'examples', and 'params' keys.
        """
        matching_fingerprints = []
        # Iterate through each fingerprint in the stored fingerprint database
        for fingerprint in self.fingerprints:
            existing_pattern = fingerprint['pattern']
            # Check if the queried MD5 hash matches the pattern of the fingerprint
            if re.match(existing_pattern, queried_md5):
                # Create a dictionary representing the matching fingerprint
                match = {
                    'description': fingerprint['description'],
                    'examples': fingerprint['examples'],
                    'params': fingerprint['params']
                }
                matching_fingerprints.append(match)

        return matching_fingerprints

    def device_fingerprinting(self, target):
        """
        Perform device fingerprinting on a target IP address or IP range.
        Args:
            target (str): The target URL or IP address or IP range.
        Returns:
            list: A list of dictionaries representing the results of device fingerprinting.
                Each dictionary contains 'IP_Address' and 'Matches' keys.
        """
        result = []
        if (len(target) > 64):
            print(f"Error: The target address {target} is too long.")            
        else:
            try:
                # Get the IP address of the target, in case URL is provided.
                ip = socket.gethostbyname(target)
                # Create an IP network object based on the IP address
                ip_network = ipaddress.ip_network(ip)
                for ip_address in ip_network:
                    ip_address = str(ip_address)
                    try:
                        # Make a request to the target IP address for the favicon.ico file
                        # Some of the hashes come from non-HTTPS addresses, so we set 'verify' to False.
                        response = requests.get("http://" + ip_address + "/favicon.ico", timeout=25, verify=False)
                        if response.status_code == 200:
                            # Calculate the MD5 hash of the response content
                            md5_hash = self.get_md5_hash(response.content)
                            # Get the matching fingerprints for the MD5 hash
                            matches = self.get_matching_fingerprints(md5_hash)
                            if matches:
                                # Add the IP address and matching fingerprints to the results
                                result.append({
                                    'IP_Address': ip_address,
                                    'Matches': matches
                                })
                            else:
                                print("Info: No match was found in the rapid7 favicons.xml database.")
                    except requests.exceptions.RequestException:
                        print(f"Error: Request made to the target address http://{ip_address}/favicon.ico is not valid.")
            except socket.gaierror:
                print(f"Error: The target address {target} is not valid.")
        return result