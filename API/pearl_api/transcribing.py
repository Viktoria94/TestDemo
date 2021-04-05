from .api import Api
from .subsystems import Subsystem

class Transcribing(Subsystem):
    def __init__(self, api):
        super(Transcribing, self).__init__(
            api,
            'transcribing')

    @property
    def status(self):
        """
        Retrieves status of transcribing,
        returns status dictionary:
        {
            'Enabled': False,
            'Paused': False,
            'SessionStartTime': 1581328096.126
        }
        """
        return self.getprop('')

    @status.setter
    def status(self, newStatus):
        """
        Sets transcribing status from dictionary:
        {
            'Enabled': False,
            'Paused': False,
        }
        """
        if not("Enabled" in newStatus or "Paused" in newStatus):
            raise Exception("New transcribing status should have Enabled and/or Paused")

        return self._api.put("transcribing", json=newStatus)

    @property
    def started(self):
        return self.status.get("Enabled", None)

    @property
    def sessionStartTime(self):
        st = self.status
        if st.get("Enabled", False):
            return st.get("SessionStartTime", None)

        return None

    @property
    def paused(self):
        return self.status.get("Paused", None)

    def start(self):
        if self.started:
            raise Exception("Session is already started")

        self.status = {
            "Enabled": True,
            "Paused": False
        }

    def stop(self):
        if not self.started:
            raise Exception("Session is not started")

        self.status = {
            "Enabled": False,
            "Paused": False,
        }

    def pause(self):
        if not self.started:
            raise Exception("Session is not started")

        if self.paused:
            raise Exception("Session is already paused")

        self.status = {
            "Enabled": True,
            "Paused": True
        }

    def resume(self):
        if not self.started:
            raise Exception("Session is not started")

        if not self.paused:
            raise Exception("Session is not paused")

        self.status = {
            "Enabled": True,
            "Paused": False
        }

    def get_prop_value(self, id):
        def find_item(items, id):
            for item in items:
                type_name = item["type"]["name"];
                item_id = item["id"]
                if (type_name == "group" or type_name == "audio_source"):
                    found_item = find_item(item["items"], id)
                    if found_item is not None:
                        return found_item
                elif item_id == id:
                    return item
            return None
        for item in self.configuration:
            items = item["items"]
            item_obj = find_item(items, id)
            if item_obj:
                return item_obj                
        return None

    def network_eth0(self):
        return self._api.get("system/network/eth0")

    def set_front_audio(self, volume):
        data = {}
        data["volume"] = volume
        self._api.post("front_audio_out/set_params", data)

    def get_front_audio(self):
        return self._api.get("front_audio_out/volume")

    def clear_button(self):
        return self._api.post("transcribing/clear")

    def enable_punctuation(self, value):
        self._api.put("transcribing/configuration/transcriber", json={'config': {"automatic_punctuation": value}})

    @property
    def configuration(self):
        return self._api.get("transcribing/configuration").json()

    @configuration.setter
    def configuration(self, params):
        self._api.put("transcribing/configuration", json={'config': params})
