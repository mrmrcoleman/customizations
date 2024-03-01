"""
Sends a webhook to the webhook handler for the Event Driven Webinar

"""

import requests
import urllib3

from extras.scripts import Script, StringVar

class TriggerEvents(Script):

    # Define the base URL
    target_url = "http://139.178.80.103:5000/webhook"

    # Data to be sent in the webhook payload
    payload = {
        'action': 'network.actions.discover_network',
    }

    class Meta:
        name = "TriggerEvents"
        description = "Send webhooks to control the Event Driven Webinar"

    webhook_endpoint = StringVar(label="Webhook Endpoint", required=True)
    action = StringVar(label="Event Action", required=True)

    def run(self, data, commit):

        webhook_endpoint = data["webhook_endpoint"]
        payload = {
            'action': data["action"],
        }

        self.log_success(f"Sending webhook to {webhook_endpoint} with payload: {payload}")

        # Suppress InsecureRequestWarning
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Send a POST request to the webhook URL with the payload
        response = requests.post(webhook_endpoint, json=payload)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            print("Webhook sent successfully")
            self.log_success("Webhook sent successfully")
        else:
            self.log_success(f"Unable send webhook. Status Code {response.status_code}")

        return