"""
Branding content
~~~~~~~
"""

from .api import Api
from .utils.collection import Collection

class Branding(object):
    """ Branding content """

    class Image(Collection.Item):
        """ Branding image """
        def __init__(self, api, info):
            id = info['id']
            super(Branding.Image, self).__init__(api, id, 'media/images/' + id, ['refs'])
            self._info = info

        @property
        def name(self):
            return self._info['name']
        
        @property
        def width(self):
            return self._info['width']

        @property
        def height(self):
            return self._info['height']

        @property
        def refs_count(self):
            return self.getprop('refs-count')

    class Images(Collection):
        """ Branding images """
        def __init__(self, api):
            super(Branding.Images, self).__init__(api, 'media/images')

        def reload(self):
            self._items = {}
            for info in self._get(''):
                id = info['id']
                self._items[id] = Branding.Image(self._api, info)

        def upload(self, file):
            # TODO: support both file object and file name
            info = self._post('', files={'file':file})
            image = Branding.Image(self._api, info)
            self._items[image.id] = image
            return image

        def delete(self, image):
            """ Delete image """
            id = str(image.id) if isinstance(image, Branding.Image) else str(image)
            ## python2/3 workaround to handle "#", "+" and " " ascii symbols in url, does not work with unicode
            import codecs
            url_id = ''.join(['%' + codecs.decode(codecs.encode(bytearray(x, 'ascii'), 'hex'), 'ascii') for x in id])
            ##
            self._delete(url_id)
            del self._items[id]

        def delete_all(self):
            """ Delete all images """
            for image in list(self._items):
                self.delete(image)

    class Media(Collection.Item):
        """ Branding image """

        def __init__(self, api, info):
            id = info['id']
            super(Branding.Image, self).__init__(api, id, 'media/images/' + id,
                                                 ['refs'])
            self._info = info

        @property
        def name(self):
            return self._info['name']

        @property
        def width(self):
            return self._info['width']

        @property
        def height(self):
            return self._info['height']

        @property
        def refs_count(self):
            return self.getprop('refs-count')

    class Images(Collection):
        """ Branding images """

        def __init__(self, api):
            super(Branding.Images, self).__init__(api, 'media/images')

        def reload(self):
            self._items = {}
            for info in self._get(''):
                id = info['id']
                self._items[id] = Branding.Image(self._api, info)

        def upload(self, file):
            # TODO: support both file object and file name
            info = self._post('', files={'file': file})
            image = Branding.Image(self._api, info)
            self._items[image.id] = image
            return image

        def delete(self, image):
            """ Delete image """
            id = str(image.id) if isinstance(image, Branding.Image) else str(
                image)
            ## python2/3 workaround to handle "#", "+" and " " ascii symbols in url, does not work with unicode
            import codecs
            url_id = ''.join(['%' + codecs.decode(
                codecs.encode(bytearray(x, 'ascii'), 'hex'), 'ascii') for x in
                              id])
            ##
            self._delete(url_id)
            del self._items[id]

        def delete_all(self):
            """ Delete all images """
            for image in list(self._items):
                self.delete(image)


    def __init__(self, api):
        self._api = api

    @property
    def images(self):
        """ Branding images """
        return Branding.Images(self._api)
    