"""
Multimedia Device Core Subsystems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from .api import Api
from .utils.api import RelativeApi
from .utils.collection import Collection


class Subsystem(RelativeApi):
    """ Simple device subsystem base:
    :param api      - REST API instance
    :param baseurl  - REST API base url
    :param props    - allowed properties
    """
    def __init__(self, api, baseurl, props=None):
        super(Subsystem, self).__init__(api, baseurl)
        self._props = props

    def getprop(self, name):
        return self._get(name)

    def __getattr__(self, name):
        if self._props == None or name in self._props:
            return self.getprop(name)   
        raise AttributeError

"""
Firmware information
"""
class Firmware(Subsystem):
    def __init__(self, api):
        super(Firmware, self).__init__(api, 'system/firmware', ['version'])

"""
Hardware information
"""
class Hardware(Subsystem):
    def __init__(self, api):
        super(Hardware, self).__init__(api, 'system/hardware', ['serial', 'mac', 'board', 'grabbers'])

"""
Storage information
"""
class Storage(Subsystem):
    def __init__(self, api):
        super(Storage, self).__init__(api, 'system/storage', ['status'])

"""
License information
"""
class License(Subsystem):
    def __init__(self, api):
        super(License, self).__init__(api, 'system/license', ['status'])

"""
Network information
"""
class Network(Subsystem):
    def __init__(self, api):
        super(Network, self).__init__(api, 'system/network', ['eth0'])


"""
Epiphan Live Dashboard information
"""
class Dashboard(Subsystem):

    class Session(Collection.Item):
        def __init__(self, api, url, id):
            super(Dashboard.Session, self).__init__(api, id, url + '%s' %(id))

        @property
        def expire(self):
            return self._get('')['expire']

    class Sessions(Collection):
        def __init__(self, api, url):
            super(Dashboard.Sessions, self).__init__(api, url)

        def reload(self):
            self._items = {}
            for s in self._get(''):
                id = s['id'];
                self._items[id] = Dashboard.Session(self._api, self._baseurl, id)

        def new(self):
            """ Add new session """
            id = self._post('')
            session = Dashboard.Session(self._api, id)
            self._items[id] = session
            return session

        def keep(self, session):
             """ Keep session alive"""
             id = str(session.id) if isinstance(session, Dashboard.Session) else str(session)
             self._put(id)
             self.reload()

        def delete(self, session):
             """ Delete session """
             id = str(session.id) if isinstance(session, Dashboard.Session) else str(session)
             self._delete(id)
             del self._items[id]

        def delete_all(self):
            """ Delete all sessions """
            for session in list(self._items):
                self.delete(session)

    def __init__(self, api):
        super(Dashboard, self).__init__(api, 'system/dashboard' )

    @property
    def layout(self):
        return self._get('layout')

    @layout.setter
    def layout(self, settings):
        return self._put('layout', json=settings)

    @property
    def sessions(self):
        return Dashboard.Sessions(self._api, self._baseurl + 'sessions')


