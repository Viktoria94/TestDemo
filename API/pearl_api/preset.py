"""
Configuration presets
~~~~~~~~~~~~~~~~~~~~~~
"""

from .api import Api
from .utils.collection import Collection


"""
Preset
"""
class Preset(Collection.Item):
    def __init__(self, api, id):
        super(Preset, self).__init__(api, id, 'system/presets/'+id, ['sections'])

    @property
    def name(self):
        """ Preset name is the same as id """
        return self._id

    @property
    def default(self):
        """ Default preset cannot be downloaded or updated """
        return self._id == 'Default'


    def download(self):
        """ Get preset content as binary buffer """
        if self.default:
            raise RuntimeError('Default cannot be downloaded')
        return self._get('')

    # TODO:
    # - apply preset


class Presets(Collection):
    def __init__(self, api):
        super(Presets, self).__init__(api, 'system/presets')

    def reload(self):
        self._items = {}
        for name in self._get(''):
            self._items[name] = Preset(self._api, name)

    def new(self, name, sections=None):
        """ Create new preset """
        data = {'name' : name}
        if sections:
            data['sections'] = sections
        name = self._post('', data)
        preset = Preset(self._api, name)
        self._items[name] = preset
        return preset

    def export(self, name, file):
        """ Export preset from file """
        # TODO: support both file object and file name
        name = self._post('', data={'name' : name}, files={'preset':file})
        preset = Preset(self._api, name)
        self._items[name] = preset
        return preset

    def apply(self, preset):
        """Activate preset"""
        name = preset.name if isinstance(preset, Preset) else preset
        self._put("active", data={'name': name})

    def delete(self, preset):
        """ Delete preset """
        name = preset.name if isinstance(preset, Preset) else preset
        ## python2/3 workaround to handle "#", "+" and " " ascii symbols in url, does not work with unicode
        import codecs
        url_name = ''.join(['%' + codecs.decode(codecs.encode(bytearray(x, 'ascii'), 'hex'), 'ascii') for x in name])
        ##
        self._delete(url_name)
        del self._items[name]

    def delete_all(self):
        """ Delete all presets """
        for preset in list(self._items.values()):
            if not preset.default:
                self.delete(preset)
