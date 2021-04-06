"""
Recorders
~~~~~~~~~
"""

from .api import Api
from .utils.collection import Collection
from .archive import Archive

"""
Recorder
"""
class Recorder(Collection.Item):
    def __init__(self, api, id):
        super(Recorder, self).__init__(api, id, 'recorders/'+id, ['name', 'started'])
        self._multichannel = False
        self._archive = Archive(api, id)

    @property
    def archive(self):
        return self._archive        

    @property
    def multichannel(self):
        return self._multichannel
    
    def start(self):
        """ Start recording """
        self._post('control/start')

    def stop(self):
        """ Stop recording """
        self._post('control/stop')

    def reset(self):
        """ Reset recording """
        self._post('control/reset')


class MultiChannelRecorder(Recorder):
    def __init__(self, api, id):
        super(MultiChannelRecorder, self).__init__(api, id)
        self._multichannel = True


class Recorders(Collection):
    def __init__(self, api):
        super(Recorders, self).__init__(api, 'recorders')

    def find(self, id):
        return self._items[id]

    def reload(self):
        self._items = {}
        for s in self._get(''):
            id = s['id'];
            if s['multisource']:
                self._items[id] = MultiChannelRecorder(self._api, id)        
            else:
                self._items[id] = Recorder(self._api, id)

    # TODO figure out way to specify channels included into recorder
    def new(self):
        id = self._post('')
        recorder = Recorder(self._api, id)
        self._items[id] = recorder
        return recorder

    def delete(self, recorder):
        """ Delete multi-channel recorder """
        id = recorder.id if isinstance(recorder, MultiChannelRecorder) else recorder
        self._delete(id)
        del self._items[id]

    def delete_all(self):
        """ Delete all recorders """
        for recorder in list(self._items):
            self.delete(recorder)
