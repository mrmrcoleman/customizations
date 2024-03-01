"""
Sends a webhook to the webhook handler for the event driven webinar

"""

import requests
import urllib3

from extras.scripts import Script

class TriggerEvents(Script):

    # Define the base URL
    target_url = "http://139.178.80.103:5000"

    # Data to be sent in the webhook payload
    payload = {
        'action': 'ping_devices',
    }

    class Meta:
        name = "TriggerEvents"
        description = "Send webhooks to control the Event Driven Webinar"

    def run(self, data, commit):

        # Suppress InsecureRequestWarning
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Send a POST request to the webhook URL with the payload
        response = requests.post(self.target_url, json=self.payload)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            print("Webhook sent successfully")
            self.log_success("Webhook sent successfully")
        else:
            self.log_success(f"Unable send webhook. Status Code {response.status_code}")

        return