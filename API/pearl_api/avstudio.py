"""
AV Studio integration
~~~~~~~
"""

from .api import Api
from .utils.collection import Collection
from utility import safe_get


class AVStudioChannel(Collection.Item):
    def __init__(self, master, channel_id):
        super(AVStudioChannel, self).__init__(
            master._api,
            channel_id,
            'avstudio/' + channel_id,
            ['status'])

        self._device_id = f'{master.master_id}-{self.id}'
        self._master = master

    @property
    def id(self):
        return self._id

    @property
    def streaming(self):
        return self._get("streaming")

    @property
    def recording(self):
        return self._get("recording")

    @property
    def device_id(self):
        return self._device_id


    @property
    def online(self):
        return safe_get(self.status, "online")


class AVStudio(Collection):
    def __init__(self, api):
        super(AVStudio, self).__init__(api, 'avstudio')

    @property
    def master_id(self):
        return self.status["master"]["id"]

    @property
    def paired(self):
        return self.status["paired"]

    @property
    def status(self):
        return self._get("")

    @property
    def enabled(self):
        return self.status["enabled"]

    @enabled.setter
    def enabled(self, value):
        self._post("config", json={"config": {"enabled": value}})

    @property
    def host(self):
        return self.status["host"]

    @host.setter
    def host(self, value):
        self._post("config", json={"config": {"host": value}})

    @property
    def lp_age(self):
        return safe_get(self.status, "master.status.lp_age")

    @property
    def online(self):
        return safe_get(self.status, "master.status.online")

    @property
    def teaminfo(self):
        return safe_get(self.status, "teaminfo")

    @property
    def channels(self):
        return [
            AVStudioChannel(self, ch["id"])
            for ch in self.status["channels"]
        ]

    def unpair(self):
        return self._delete("")