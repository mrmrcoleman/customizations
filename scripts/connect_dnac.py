"""
This script connects to Cisco DNAC and returns a list of the available devices.

It expects to find the following environment variables present and will exit if both are not set in the environment:

DNAC_USERNAME
DNAC_PASSWORD
"""

# The commented out imports break NBC
#import requests
#import urllib3
#import base64
#import json
import os
import sys

from extras.scripts import Script

class GetDNACDevices(Script):

    def get_auth_token(self, username, password):
        # Complete URL for the authentication endpoint
        url = self.base_url + "system/api/v1/auth/token"
        # Encode the username and password in Base64 for the Authorization header
        credentials = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')
        headers = {'Content-Type': 'application/json', 'Authorization': f'Basic {credentials}'}
        with requests.Session() as session:
            response = session.post(url, headers=headers, verify=False)
            if response.status_code == 200:
                token_info = response.json()
                return token_info.get('Token')
            else:
                raise Exception(f"Error: Unable to fetch token, status code {response.status_code}")

    class Meta:
        name = "GetDNACDevices"
        description = "Connect to a DNAC instance and return the available devices"

    def run(self, data, commit):

        for name, value in os.environ.items():
            self.log_success("{0}: {1}".format(name, value))

        return