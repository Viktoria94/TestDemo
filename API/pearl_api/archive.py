"""
Archive
~~~~~~~~~
"""

from .api import Api
from .utils.collection import Collection

"""
Archive
"""
class Archive:
    """ Archive """
    class File(Collection.Item):
        """ Archive file """
        def __init__(self, api, info):
            id = info['id']
            recorder_id = info['recorder']
            super(Archive.File, self).__init__(api, id, 'recorders/'+recorder_id+'/archive/files/' + id, [])
            self._info = info

        @property
        def name(self):
            return self._info['name']

        @name.setter
        def name(self, name):
            return self._put('name', {'name': name})

        @property
        def extension(self):
            return self._info['extension']

        @property
        def created(self):
            import dateutil.parser
            return dateutil.parser.parse(self._info['created'])

        @property
        def duration(self):
            from datetime import timedelta
            return timedelta(seconds=self._info['duration'])

        @property
        def size(self):
            return self._info['size']

        @property
        def downloaded(self):
            return self._info['downloaded']

        # TODO: implement other properties

    class Files(Collection):
        """ Archive files """
        def __init__(self, api, recorder_id):
            super(Archive.Files, self).__init__(api, 'recorders/'+recorder_id+'/archive/files')

        def reload(self):
            self._items = {}
            for f in self._get(''):
                id = f['id']
                self._items[id] = Archive.File(self._api, f)

        def delete(self, file):
            id = str(file.id) if isinstance(file, Archive.File) else str(file)
            self._delete(id)
            del self._items[id]

        def delete_some(self, files):
            id_list = []
            for f in files:
                id_list.append( str(f.id) if isinstance(f, Archive.File) else str(f) )
            self._post('control/delete', json=id_list)
            for id in id_list:
                del self._items[id]

        def delete_all(self):
            self._post('control/delete-all')
            self._items = {}


    def __init__(self, api, recorder_id):
        self._api = api
        self._recorder_id = recorder_id

    @property
    def files(self):
        return Archive.Files(self._api, self._recorder_id)

    # TODO: consider get last recorded file id

    # TODO: access to file range (from,limit)
