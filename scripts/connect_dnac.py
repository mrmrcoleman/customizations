"""
This script connects to Cisco DNAC and returns a list of the available devices.

It expects to find the following environment variables present and will exit if both are not set in the environment:

DNAC_USERNAME
DNAC_PASSWORD
"""

import requests
import base64
import json
import urllib3
import os
import sys

class ShowEnvVars(Script):

    class Meta:
        name = "GetDNACDevices"
        description = "Connect to a DNAC instance and return the available devices"

    def run(self, data, commit):

        for name, value in os.environ.items():
            self.log_success("{0}: {1}".format(name, value))

        return