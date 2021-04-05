"""
Internal utilities: Collection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from ..api import Api
from .api import RelativeApi


"""
Generic id-based collection of items
"""
class Collection(RelativeApi):
    """
    Item
    """
    class Item(RelativeApi):
        def __init__(self, api, id, url, props=None):
            super(Collection.Item, self).__init__(api, url)
            self._id = id
            self._props = props

        @property
        def id(self):
            return self._id

        """
        Retrieve property via REST API
        """
        def getprop(self, name):
            return self._get(name)

        """
        Automatically retrieve property via REST API
        """
        def __getattr__(self, name):
            if self._props == None or name in self._props:
                return self.getprop(name)   
            raise AttributeError        

    """
    Initialize collection
    """
    def __init__(self, api, url, **kwargs):
        super(Collection,self).__init__(api, url, **kwargs)
        self.reload()

    """
    Reload collection
        Must be overloaded
    """
    def reload(self):
       self._items = {}

    def __getitem__(self, key):
        return self._items[key]

    def __iter__(self):
        return self._items.values().__iter__()        

    def __len__(self):
        return len(self._items)
