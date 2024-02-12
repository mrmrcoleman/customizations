"""
This script connects to Cisco DNAC and returns a list of the available devices.

It expects to find the following environment variables present and will exit if both are not set in the environment:

DNAC_USERNAME
DNAC_PASSWORD
"""

import requests
import urllib3
import base64
import json
import os
import sys

from extras.scripts import Script

class GetDNACDevices(Script):

    # Define the base URL
    base_url = "https://sandboxdnac.cisco.com/dna/"

    class Meta:
        name = "GetDNACDevices"
        description = "Connect to a DNAC instance and return the available devices"

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
            
    def get_device_information(self, token):
        # Complete URL for the device information endpoint
        url = self.base_url + "intent/api/v1/network-device"
        headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
        with requests.Session() as session:
            response = session.get(url, headers=headers, verify=False)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error: Unable to fetch device information, status code {response.status_code}")
        
    def get_dnac_credentials(self) -> tuple[str, str]:
        if os.getenv("SECRET_DNAC_USERNAME", None) == None:
            self.log_failure("SECRET_DNAC_USERNAME environment variable not set. Exiting. Example: 'export SECRET_DNAC_USERNAME=devnetuser'")
        else:
            dnac_username = os.getenv("SECRET_DNAC_USERNAME")

        if os.getenv("SECRET_DNAC_PASSWORD", None) == None:
            self.log_failure("SECRET_DNAC_PASSWORD environment variable not set. Exiting. Example= 'export SECRET_DNAC_PASSWORD=Cisco123!'")
        else:
            dnac_password = os.getenv("SECRET_DNAC_PASSWORD")

        return dnac_username, dnac_password

    def run(self, data, commit):

        # Suppress InsecureRequestWarning
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        try:
            username, password = self.get_dnac_credentials()
            token = self.get_auth_token(username, password)
            device_information = self.get_device_information(token)
            self.log_success(json.dumps(device_information, indent=4))
        except Exception as e:
            print(e)

        return