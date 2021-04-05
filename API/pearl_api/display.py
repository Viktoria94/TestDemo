"""
Displays
~~~~~~~~~
"""

from .api import Api
from .utils.collection import Collection


"""
Display
"""
class Display(Collection.Item):
    def __init__(self, api, id):
        super(Display, self).__init__(api, id, 'displays/'+id, ['name', 'status', 'preview', 'settings'])

    def update(self, settings, save=True):
        return self._patch('settings', json=settings)


class Displays(Collection):
    def __init__(self, api):
        super(Displays, self).__init__(api, 'displays')

    def reload(self):
        self._items = {}
        for s in self._get(''):
            id = s['id'];
            self._items[id] = Display(self._api, id)
