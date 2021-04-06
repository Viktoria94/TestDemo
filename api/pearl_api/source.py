"""
Sources
~~~~~~~

"""

from .api import Api
from .utils.collection import Collection

"""
Source base
"""
class Source(Collection.Item):
    def __init__(self, api, info):
        id = info['id']
        super(Source, self).__init__(api, id, 'sources/'+id, ['name', 'status', 'preview'])
        self._type  = info['type']
        self._auto  = info.get('auto', False)
        self._video = info.get('video', False)
        self._audio = info.get('audio', False)

    """ Permanent properties """
    @property
    def type(self):
        return self._type

    @property
    def auto(self):
        return self._auto

    @property
    def video(self):
        return self._video

    @property
    def audio(self):
        return self._audio


# TODO: different type of sources
class LocalSource(Source):
    def __init__(self, api, info):
        super(LocalSource, self).__init__(api, info)

class LocalAudioSource(Source):
    def __init__(self, api, info):
        super(LocalAudioSource, self).__init__(api, info)

class RTSPSource(Source):
    def __init__(self, api, info):
        super(RTSPSource, self).__init__(api, info)

class UVCSource(Source):
    def __init__(self, api, info):
        super(UVCSource, self).__init__(api, info)

class AutoSource(Source):
    def __init__(self, api, info):
        super(AutoSource, self).__init__(api, info)

class ChannelSource(Source):
    def __init__(self, api, info):
        super(ChannelSource, self).__init__(api, info)


"""
Sources
"""
class Sources(Collection):
    def __init__(self, api):
        super(Sources, self).__init__(api, 'sources', params='?channels=true')

    def reload(self):
        self._items = {}
        for s in self._get(''):
            self._add_source(s)

    def _add_source(self, info):
        p = None
        if info['type'] == 'local':
            p = LocalSource(self._api, info )
        elif info['type'] == 'local-audio':
            p = LocalAudioSource(self._api, info )
        elif info['type'] == 'network':
            p = RTSPSource(self._api, info )
        elif info['type'] == 'usb':
            p = UVCSource(self._api, info )
        elif info['type'] == 'auto':
            p = AutoSource(self._api, info )
        elif info['type'] == 'channel':
            p = ChannelSource(self._api, info)
        else:
            p = Source(self._api, info )
        if p is not None:
            self._items[info['id']] = p
        return p

    #TODO add method to create RTSP soures when REST api is available
    def new(self, type):
        """ Creates new source, applicable for RTSP sources """
        pass
