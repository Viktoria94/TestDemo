"""
Multimedia Devices Control library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Direct REST api Access

md.Api is REST api caller for Multimedia Devices (Grid/Pearl/Pearl-2)
usage:
   >>> import md
   >>> api = md.Api('10.0.0.1')
   >>> r = api.get('system/firmware/version')
   >>> r
   4.3.0a


2. Device access

md.Device provides convenient access to major device properties, like hardware, firmware, sources, channels, etc.
usage:
   >>> import md
   >>> device = md.Device('10.0.0.1')
   >>> device.firmware.version
   4.3.0a


Requirements:
  - requests (python-requests.org)
  - Pillow   (python-pillow.org)
  - dateutil (pypi.python.org/pypi/python-dateutil/2.6.0)

Minimum firmware version:
 - 4.3.0

Additional information:
  - https://office.epiphan.com:8451/display/MD/REST+API%3A+4.3.0#RESTAPI:4.3.0-Pythonlibrary

"""

__title__   = 'Multimedia Devices Control'
__version__ = '0.1'
__author__  = 'Roman Davydov'

# Errors
from .api import Error, ServerError, NotFound, Forbidden
# REST api
from .api import Api
# Device api
from .device import Device

from .remote_login_tunnel import RemoteLoginTunnel

from .paired_pearl import PairedPearl
