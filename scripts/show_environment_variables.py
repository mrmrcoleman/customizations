"""
This simple script shows all the environment variables in the current environment and is useful for debugging.
"""

from extras.scripts import *
from django.utils.text import slugify

from dcim.choices import DeviceStatusChoices, SiteStatusChoices
from dcim.models import Device, DeviceRole, DeviceType, Site

import os

class ShowEnvVars(Script):

    class Meta:
        name = "Display ENV VARs"
        description = "Display ENV VARs"

    def run(self, data, commit):

        for name, value in os.environ.items():
            self.log_success("{0}: {1}".format(name, value))

        return