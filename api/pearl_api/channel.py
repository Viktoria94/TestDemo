"""
Channels
~~~~~~~
"""

from .api import Api
from .utils.collection import Collection
from .recorder import Recorder


"""
Layout
"""
class Layout(Collection.Item):

    def __init__(self, api, channel, id):
        super(Layout,self).__init__(api, id, 'channels/%s/layouts/%s' %(channel.id, id), ['active'])
        self._channel = channel

    @property
    def channel(self):
        return self._channel

    @property
    def name(self):
        return self.getprop('name')

    @name.setter
    def name(self, name):
        """Rename layout"""
        return self._put('name', {'name': name})

    @property
    def body(self):
        return self._get('settings')

    @body.setter
    def body(self, settings):
        return self._put('settings', json=settings)


class Layouts(Collection):
    def __init__(self, api, channel):
        self._channel = channel
        super(Layouts, self).__init__(api, 'channels/'+self._channel.id+'/layouts')

    def reload(self):
        self._items = {}
        for s in self._get(''):
            id = s['id'];
            #self._items[id.encode()] = Layout(self._api, self._channel, id) #added encode
            self._items[id] = Layout(self._api, self._channel, id)

    def new(self):
        """ Add new layout """
        id = self._post('')
        layout = Layout(self._api, self._channel, id)
        self._items[id] = layout
        return layout

    def clone(self, layout):
        """ Clone channel """
        src = str(layout.id) if isinstance(layout, Layout) else str(layout)
        id = self._post('', {'source' : src })
        layout = Layout(self._api, self._channel, id)
        self._items[id] = layout
        return layout

    def delete(self, layout):
        """ Delete layout """
        id = str(layout.id) if isinstance(layout, Layout) else str(layout)
        self._delete(id)
        del self._items[id]

    @property
    def order(self):
        """Get order of layouts"""
        """:returns: array of identifiers"""
        return self._get('order')

    @order.setter
    def order(self, order):
        """Set order of layouts"""
        """ :param order: comma-separated list or an array of identifiers """
        order = ','.join(order) if isinstance(order, list) else order
        return self._put('order', {'order' : order})

    @property
    def active(self):
        """Get active layout id"""
        """:returns: identifier as string"""
        return self._get('active')

    @active.setter
    def active(self, layout_id):
        """Set active layout"""
        """ :param order: layout identifier as string """
        return self._put('active', {'id': str(layout_id)})


"""
Publisher
"""
class Publisher(Collection.Item):
    def __init__(self, api, channel, id):
        super(Publisher,self).__init__(api, id, 'channels/%s/publishers/%s' %(channel.id, id), ['type', 'name', 'status', 'settings'])
        self._channel = channel

    @property
    def channel(self):
        return self._channel

    @property
    def name(self):
        return self._get('name')

    @property
    def status(self):
        return self._get('status')

    @property
    def type(self):
        return self._get('type')

    @property
    def settings(self):
        return self._get('settings')

    def update(self, settings, save=True):
        return self._patch('settings', json=settings)

    def save(self):
        return self._post('settings/save')


class CDNPublisher(Publisher):
    """ RTMP/RTSP publisher """
    def __init__(self, api, channel, id):
        super(CDNPublisher, self).__init__(api, channel, id)

    def start(self):
        """ Start publishing """
        self._api.post(self._baseurl + 'control/start')

    def stop(self):
        """ Stop publishing """
        self._api.post(self._baseurl + 'control/stop')


class RTSPPublisher(CDNPublisher):
    def __init__(self, api, channel, id):
        super(RTSPPublisher, self).__init__(api, channel, id)


    def update(self, URL, transport, username, password, singletouch=True):
        """ Update publisher """
        return super(RTSPPublisher, self).update( {'type': self.type,
                                                  'url': URL,
                                                  'transport' : transport,  #tcp or udp
                                                  'username': username,
                                                  'password': password,
                                                  'single-touch': singletouch} )

class RTMPPublisher(CDNPublisher):
    def __init__(self, api, channel, id):
        super(RTMPPublisher, self).__init__(api, channel, id)


    def update(self, URL, stream, username, password, singletouch=True):
        """ Update publisher """
        return super(RTMPPublisher, self).update( {'type': self.type,
                                                  'url': URL,
                                                  'stream': stream,
                                                  'username': username,
                                                  'password': password,
                                                  'single-touch': singletouch} )

class MulticastPublisher(Publisher):
    """ Multicast publisher """
    def __init__(self, api, channel, id):
        super(MulticastPublisher, self).__init__(api, channel, id)

class RTPUDPPublihser(MulticastPublisher):
    """ RTP/UDP Multicast publisher """
    def __init__(self, api, channel, id):
        super(RTPUDPPublihser, self).__init__(api, channel, id)

    def update(self, destIP, audioPort, videoPort):
        """" Update publisher """
        return super(RTPUDPPublihser, self).update({'type': self.type,
                                                    'address': destIP,
                                                    'audio-port': audioPort,
                                                    'video-port': videoPort })

class MPEGTSUDPPublisher(MulticastPublisher):
    """ MPEG-TS UDP Multicast publisher """
    def __init__(self, api, channel, id):
        super(MPEGTSUDPPublisher, self).__init__(api, channel, id)

    def update(self, destIP, destPort, sap, sapIP, sapChannel, sapGroup):
        """ Update publisher """
        return super(MPEGTSUDPPublisher, self).update({'type': self.type,
                                                       'address': destIP,
                                                       'port': destPort,
                                                       'sap': sap,
                                                       'sap-ip': sapIP,
                                                       'sap-channel': sapChannel,
                                                       'sap-play-group': sapGroup})

class MPEGTSRTPPublisher(MulticastPublisher):
    """ MPEG-TS RTP Multicast publisher """
    def __init__(self, api, channel, id):
        super(MPEGTSRTPPublisher, self).__init__(api, channel, id)

    def update(self, destIP, destPort, sap, sapIP, sapChannel, sapGroup):
        """ Update publisher """
        return super(MPEGTSRTPPublisher, self).update({'type': self.type,
                                                       'address': destIP,
                                                       'port': destPort,
                                                       'sap': sap,
                                                       'sap-ip': sapIP,
                                                       'sap-channel': sapChannel,
                                                       'sap-play-group': sapGroup})

class Publishers(Collection):
    def __init__(self, api, channel):
        self._channel = channel
        super(Publishers, self).__init__(api, 'channels/'+self._channel.id+'/publishers')

    def reload(self):
        self._items = {}
        for s in self._get('type'):
            self._add_publisher(s['id'], s['type'])

    def _add_publisher(self, id, type):
            p = None
            if type == 'rtsp':
                p = RTSPPublisher(self._api, self._channel, id)
            elif type == 'rtmp':
                p = RTMPPublisher(self._api, self._channel, id)
            elif type == 'rtp-udp':
                p = RTPUDPPublihser(self._api, self._channel, id)
            elif type == 'mpegts-udp':
                p = MPEGTSUDPPublisher(self._api, self._channel, id)
            elif type == 'mpegts-rtp':
                p = MPEGTSRTPPublisher(self._api, self._channel, id)
            else:
                p = Publisher(self._api, self._channel, id)
            if p is not None:
                self._items[id] = p
            return p

    def status(self):
        "get publisher status"
        return self._get('status')

    def start(self):
        """ Start all publishers """
        self._post('control/start')

    def stop(self):
        """ Stop all publishers """
        self._post('control/stop')

    def new(self, type=None, **kwargs):
        """ Add new publisher """
        files = kwargs.get('files', None)
        if files:
            p = self._post('', files=files)
            return self._add_publisher(str(p['id']), 'rtmp')    #TODO: rework assuming that only RTMP push is created from xml file
        else:
            p = self._post('', {'type': type})
            return self._add_publisher(str(p['id']), type)

    def delete(self, publisher):
        """ Delete publisher """
        id = str(publisher.id) if isinstance(publisher, Publisher) else str(publisher)
        self._delete(id)
        del self._items[id]

    def delete_all(self):
        """ Delete all publishers """
        for publisher in list(self._items):
            self.delete(publisher)

"""
Encoder
"""
class Encoder(Collection.Item):
    def __init__(self, api, id, enc_id):
        super(Encoder, self).__init__(
            api, 
            id, 
            'channels/{}/encoders/{}'.format(id, enc_id), 
            ['type', 'status', 'settings'])

"""
Channel
"""
class Channel(Collection.Item):
    def __init__(self, api, id):
        super(Channel, self).__init__(api, id, 'channels/'+id, ['name', 'status', 'preview', 'connections'])
        self._recorder = Recorder(api, id)

    @property
    def name(self):
        return self._get('name')

    @name.setter
    def name(self, name):
        return self._put('name', {"name": name})

    @property
    def layouts(self):
        return Layouts(self._api, self)

    @property
    def publishers(self):
        return Publishers(self._api, self)

    @property
    def recorder(self):
        return self._recorder

    @property
    def encoders(self):
        enc_dict = self._get('encoders')
        return [Encoder(self._api, self._id, enc["id"]) for enc in enc_dict]

class Channels(Collection):
    def __init__(self, api):
        super(Channels, self).__init__(api, 'channels')

    def reload(self):
        self._items = {}
        for s in self._get(''):
            id = s['id']
            self._items[id] = Channel(self._api, id)

    def new(self):
        id = self._post('')
        channel = Channel(self._api, id)
        self._items[id] = channel
        return channel

    def clone(self, channel):
        """ Clone channel """
        src = str(channel.id) if isinstance(channel, Channel) else str(channel)
        id = self._post('', {'source' : src })
        channel = Channel(self._api, id)
        self._items[id] = channel
        return channel

    def delete(self, channel):
        """ Delete channel """
        id = str(channel.id) if isinstance(channel, Channel) else str(channel)
        self._delete(id)
        del self._items[id]

    def delete_all(self):
        """ Delete all channels """
        for channel in list(self._items):
            self.delete(channel)

    @property
    def connections_summary(self):
        return self._get('connections/summary')
