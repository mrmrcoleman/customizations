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

class ShowEnvVars(Script):

    class Meta:
        name = "GetDNACDevices"
        description = "Connect to a DNAC instance and return the available devices"

    def run(self, data, commit):

        # Suppress InsecureRequestWarning
        #urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        for name, value in os.environ.items():
            self.log_success("{0}: {1}".format(name, value))

        return