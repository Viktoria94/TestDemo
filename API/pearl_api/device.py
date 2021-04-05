"""
Multimedia Devices Controller
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from .api import Api
from .subsystems import Firmware, Hardware, Storage, License, Dashboard, Network
from .source import Sources
from .channel import Channels
from .recorder import Recorders
from .display import Displays
from .preset import Presets
from .branding import Branding
from .avstudio import AVStudio
from .transcribing import Transcribing

class Device(object):
    def __init__(self, address, role=Api.Role(Api.Role.Admin, ''), protocol='http'):
        self._api = Api(address, role, protocol)
        # Subsystems
        self._firmware  = Firmware(self._api)
        self._hardware  = Hardware(self._api)
        self._storage   = Storage(self._api)
        self._branding  = Branding(self._api)
        self._license = License(self._api)
        self._avstudio = AVStudio(self._api)
        self._network = Network(self._api)
        self._transcribing = Transcribing(self._api)


    @property
    def api(self):
        return self._api

    """ Status """
    @property
    def status(self):
        return self._api.get('system/status')
    

    """ Subsystems """
    @property
    def firmware(self):
        return self._firmware
    
    @property
    def hardware(self):
        return self._hardware

    @property
    def storage(self):
        return self._storage

    @property
    def license(self):
        return self._license

    @property
    def dashboard(self):
        return Dashboard(self._api)

    @property
    def sources(self):
        """ Sources """
        return Sources(self._api)
    
    @property
    def channels(self):
        """ Channels """
        return Channels(self._api)

    @property 
    def recorders(self):
        """ Recorders """
        return Recorders(self._api)

    @property 
    def displays(self):
        """ Displays """
        return Displays(self._api)    

    @property
    def presets(self):
        """ Configuration presets """
        return Presets(self._api)

    @property
    def branding(self):
        """ Branding content """
        return self._branding

    @property
    def network(self):
        """ Network content """
        return self._network

    @property
    def avstudio(self):
        """ AV Studio content """
        return self._avstudio

    @property
    def transcribing(self):
        """ Transcribing """
        return self._transcribing
    
